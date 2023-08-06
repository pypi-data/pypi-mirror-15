from __future__ import print_function
import hashlib, json, random, select, socket, struct, sys, traceback, warnings
from collections import namedtuple, deque
from .base import flags, user_salt, compression, to_base_58, from_base_58, \
        getUTC, compress, decompress, intersect, get_lan_ip, protocol, \
        base_connection, base_daemon, base_socket, message, pathfinding_message

max_outgoing = 4
default_protocol = protocol('mesh', "Plaintext")  # SSL")

class mesh_connection(base_connection):
    def found_terminator(self):
        """Processes received messages"""
        raw_msg = ''.encode().join(self.buffer)
        self.expected = 4
        self.buffer = []
        self.active = False
        reply_object = self
        try:
            msg = pathfinding_message.feed_string(self.protocol, raw_msg, False, self.compression)
        except (IndexError, struct.error):
            self.__print__("Failed to decode message: %s. Expected compression: %s." % \
                            (raw_msg, intersect(compression, self.compression)[0]), level=1)
            self.send(flags.renegotiate, flags.compression, json.dumps([]))
            self.send(flags.renegotiate, flags.resend)
            return
        packets = msg.packets
        self.__print__("Message received: %s" % packets, level=1)
        if packets[0] == flags.waterfall:
            if packets[2] in (i for i, t in self.server.waterfalls):
                self.__print__("Waterfall already captured", level=2)
                return
            elif from_base_58(packets[3]) < getUTC() - 60:
                self.__print__("Waterfall expired", level=2)
                return
            self.__print__("New waterfall received. Proceeding as normal", level=2)
            reply_object = packets[1]
        elif packets[0] == flags.renegotiate:
            if packets[4] == flags.compression:
                encoded_methods = [algo.encode() for algo in json.loads(packets[5].decode())]
                respond = (self.compression != encoded_methods)
                self.compression = encoded_methods
                self.__print__("Compression methods changed to: %s" % repr(self.compression), level=2)
                if respond:
                    decoded_methods = [algo.decode() for algo in intersect(compression, self.compression)]
                    self.send(flags.renegotiate, flags.compression, json.dumps(decoded_methods))
                return
            elif packets[4] == flags.resend:
                self.send(*self.last_sent)
                return
        self.server.handle_msg(message(msg, self.server), reply_object)

    def send(self, msg_type, *args, **kargs):
        """Sends a message through its connection. The first argument is message type. All after that are content packets"""
        # This section handles waterfall-specific flags
        id = kargs.get('id', self.server.id)  # Latter is returned if key not found
        time = kargs.get('time', getUTC())
        # Begin real method
        msg = pathfinding_message(self.protocol, msg_type, id, list(args), self.compression)
        if (msg.id, msg.time) not in self.server.waterfalls:
            self.server.waterfalls.appendleft((msg.id, msg.time))
        if msg_type in [flags.whisper, flags.broadcast]:
            self.last_sent = [msg_type] + list(args)
        self.__print__("Sending %s to %s" % ([msg.len] + msg.packets, self), level=4)
        if msg.compression_used: self.__print__("Compressing with %s" % msg.compression_used, level=4)
        try:
            self.sock.send(msg.string)
        except (IOError, socket.error) as e:
            self.server.daemon.exceptions.append((e, traceback.format_exc()))
            self.server.disconnect(self)


class mesh_daemon(base_daemon):
    def handle_accept(self):
        """Handle an incoming connection"""
        if sys.version_info >= (3, 3):
            exceptions = (socket.error, ConnectionError)
        else:
            exceptions = (socket.error, )
        try:
            conn, addr = self.sock.accept()
            if conn is not None:
                self.__print__('Incoming connection from %s' % repr(addr), level=1)
                handler = mesh_connection(conn, self.server, self.protocol)
                compression_to_send = [method.decode() for method in compression]
                handler.send(flags.whisper, flags.handshake, self.server.id, self.protocol.id, json.dumps(self.server.out_addr),\
                             json.dumps(compression_to_send))
                handler.sock.settimeout(1)
                self.server.awaiting_ids.append(handler)
                # print("Appended ", handler.addr, " to handler list: ", handler)
            else:
                self.__print__("Somehow the handle_accept got triggered", level=1)
        except exceptions:
            pass

    def mainloop(self):
        """Daemon thread which handles all incoming data and connections"""
        while self.alive:
            # for handler in list(self.server.routing_table.values()) + self.server.awaiting_ids:
            if list(self.server.routing_table.values()) + self.server.awaiting_ids:
                for handler in select.select(list(self.server.routing_table.values()) + self.server.awaiting_ids, [], [], 0.01)[0]:
                    # print("Collecting data from %s" % repr(handler))
                    try:
                        while not handler.find_terminator():
                            if not handler.collect_incoming_data(handler.sock.recv(1)):
                                self.__print__("disconnecting node %s while in loop" % handler.id, level=6)
                                self.disconnect(handler)
                                self.server.request_peers()
                                raise socket.timeout()  # Quick, error free breakout
                        handler.found_terminator()
                    except socket.timeout:
                        continue  # Shouldn't happen with select, but if it does...
                    except Exception as e:
                        if isinstance(e, socket.error) and e.args[0] in (9, 104, 10053, 10054, 10058):
                            node_id = handler.id
                            if not node_id:
                                node_id = repr(handler)
                            self.__print__("Node %s has disconnected from the network" % node_id, level=1)
                        else:
                            self.__print__("There was an unhandled exception with peer id %s. This peer is being disconnected, and the relevant exception is added to the debug queue. If you'd like to report this, please post a copy of your mesh_socket.daemon.exceptions list to github.com/gappleto97/python-utils." % handler.id, level=0)
                            self.exceptions.append((e, traceback.format_exc()))
                        self.disconnect(handler)
                        self.server.request_peers()
            self.handle_accept()


class mesh_socket(base_socket):
    def __init__(self, addr, port, prot=default_protocol, out_addr=None, debug_level=0):
        self.protocol = prot
        self.debug_level = debug_level
        self.routing_table = {}     # In format {ID: handler}
        self.awaiting_ids = []      # Connected, but not handshook yet
        self.requests = {}          # Metadata about message replies where you aren't connected to the sender
        self.waterfalls = deque()   # Metadata of messages to waterfall
        self.queue = deque()        # Queue of received messages. Access through recv()
        if out_addr:                # Outward facing address, if you're port forwarding
            self.out_addr = out_addr
        elif addr == '0.0.0.0':
            self.out_addr = get_lan_ip(), port
        else:
            self.out_addr = addr, port
        info = [str(self.out_addr).encode(), prot.id, user_salt]
        h = hashlib.sha384(b''.join(info))
        self.id = to_base_58(int(h.hexdigest(), 16))
        self.daemon = mesh_daemon(addr, port, self, prot)

    def handle_msg(self, msg, handler):
        """Decides how to handle various message types, allowing some to be handled automatically"""
        packets = msg.packets
        if packets[0] == flags.handshake:
            self.__handle_handshake(packets, handler)
        elif packets[0] == flags.peers:
            self.__handle_peers(packets, handler)
        elif packets[0] == flags.response:
            self.__handle_response(packets, handler)
        elif packets[0] == flags.request:
            self.__handle_request(packets, handler)
        elif packets[0] == flags.whisper or self.waterfall(msg):
            self.queue.appendleft(msg)

    def __get_peer_list(self):
        peer_list = [(self.routing_table[key].addr, key.decode()) for key in self.routing_table]
        random.shuffle(peer_list)
        return peer_list

    def __resolve_connection_conflict(self, handler, h_id):
        self.__print__("Resolving peer conflict on id %s" % repr(h_id), level=1)
        to_keep, to_kill = None, None
        if bool(from_base_58(self.id) > from_base_58(h_id)) ^ bool(handler.outgoing):  # logical xor
            self.__print__("Closing outgoing connection", level=1)
            to_keep, to_kill = self.routing_table[h_id], handler
            self.__print__(to_keep.outgoing, level=1)
        else:
            self.__print__("Closing incoming connection", level=1)
            to_keep, to_kill = handler, self.routing_table[h_id]
            self.__print__(not to_keep.outgoing, level=1)
        self.disconnect(to_kill)
        self.routing_table.update({h_id: to_keep})

    def __handle_handshake(self, packets, handler):
        if packets[2] != self.protocol.id:
            self.disconnect(handler)
            return
        elif handler is not self.routing_table.get(packets[1], handler):
            self.__resolve_connection_conflict(handler, packets[1])
        handler.id = packets[1]
        handler.addr = json.loads(packets[3].decode())
        handler.compression = json.loads(packets[4].decode())
        handler.compression = [algo.encode() for algo in handler.compression]
        self.__print__("Compression methods changed to %s" % repr(handler.compression), level=4)
        if handler in self.awaiting_ids:
            self.awaiting_ids.remove(handler)
        self.routing_table.update({packets[1]: handler})
        handler.send(flags.whisper, flags.peers, json.dumps(self.__get_peer_list()))

    def __handle_peers(self, packets, handler):
        new_peers = json.loads(packets[1].decode())
        for addr, id in new_peers:
            if len(self.outgoing) < max_outgoing and addr:
                try:
                    self.connect(addr[0], addr[1], id.encode())
                except:  # pragma: no cover
                    self.__print__("Could not connect to %s:%s because\n%s" % (addr[0], addr[1], traceback.format_exc()), level=1)
                    continue

    def __handle_response(self, packets, handler):
        self.__print__("Response received for request id %s" % packets[1], level=1)
        if self.requests.get(packets[1]):
            addr = json.loads(packets[2].decode())
            if addr:
                msg = self.requests.get(packets[1])
                self.requests.pop(packets[1])
                self.connect(addr[0][0], addr[0][1], addr[1])
                self.routing_table[addr[1]].send(*msg)

    def __handle_request(self, packets, handler):
        if packets[1] == '*'.encode():
            handler.send(flags.whisper, flags.peers, json.dumps(self.__get_peer_list()))
        elif self.routing_table.get(packets[2]):
            handler.send(flags.broadcast, flags.response, packets[1], json.dumps([self.routing_table.get(packets[2]).addr, packets[2].decode()]))

    def send(self, *args, **kargs):
        """Sends data to all peers. type flag will override normal subflag. Defaults to 'broadcast'"""
        # self.cleanup()
        send_type = kargs.pop('type', flags.broadcast)
        main_flag = kargs.pop('flag', flags.broadcast)
        # map(methodcaller('send', 'broadcast', 'broadcast', *args), self.routing_table.values())
        handlers = list(self.routing_table.values())
        for handler in handlers:
            handler.send(main_flag, send_type, *args)

    def __clean_waterfalls(self):
        """Cleans up the waterfall deque"""
        self.waterfalls = deque(set(self.waterfalls))
        self.waterfalls = deque((i for i in self.waterfalls if i[1] > getUTC() - 60))

    def waterfall(self, msg):
        """Handles the waterfalling of received messages"""
        # self.cleanup()
        # self.__print__(msg.id, [i for i, t in self.waterfalls], level=5)
        if msg.id not in (i for i, t in self.waterfalls):
            self.waterfalls.appendleft((msg.id, msg.time))
            for handler in self.routing_table.values():
                if handler.id != msg.sender:
                    handler.send(flags.waterfall, *msg.packets, time=msg.time_58, id=msg.sender)
            self.__clean_waterfalls()
            return True
        else:
            self.__print__("Not rebroadcasting", level=3)
            return False

    def connect(self, addr, port, id=None):
        """Connects to a specified node. Specifying ID will immediately add to routing table. Blocking"""
        # self.cleanup()
        self.__print__("Attempting connection to %s:%s with id %s" % (addr, port, repr(id)), level=1)
        if socket.getaddrinfo(addr, port)[0] == socket.getaddrinfo(*self.out_addr)[0] or \
                                                            id in self.routing_table:
            self.__print__("Connection already established", level=1)
            return False
        if self.protocol.encryption == "Plaintext":
            conn = socket.socket()
        elif self.protocol.encryption == "SSL":
            from . import ssl_wrapper
            conn = ssl_wrapper.get_socket(False)
        elif self.protocol.encryption == "PKCS1_v1.5":
            from . import net
            warnings.warn("The net module is scheduled to be deprecated in the next release", DeprecationWarning)
            conn = net.secure_socket(silent=True)
        else:
            raise ValueError("Unkown encryption method")
        conn.settimeout(1)
        conn.connect((addr, port))
        handler = mesh_connection(conn, self, self.protocol, outgoing=True)
        handler.id = id
        compression_to_send = [method.decode() for method in compression]
        handler.send(flags.whisper, flags.handshake, self.id, self.protocol.id, json.dumps(self.out_addr),\
                    json.dumps(compression_to_send))
        if not id:
            self.awaiting_ids.append(handler)
        else:
            self.routing_table.update({id: handler})
        # print("Appended ", port, addr, " to handler list: ", handler)

    def disconnect(self, handler):
        """Disconnects a node"""
        node_id = handler.id
        if not node_id:
            node_id = repr(handler)
        self.__print__("Connection to node %s has been closed" % node_id, level=1)
        if handler in self.awaiting_ids:
            self.awaiting_ids.remove(handler)
        elif self.routing_table.get(handler.id) is handler:
            self.routing_table.pop(handler.id)
        try:
            handler.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass

    def request_peers(self):
        self.send('*', type=flags.request, flag=flags.whisper)