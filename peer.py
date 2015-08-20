import socket

from utils import log
from node import Node
from requestfactory import RequestFactory
from rpc import Ping, Pong, LocalFindNode

class Peer:
    def __init__(self, node, port):
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.socket.bind(('', port))
      self.node = node

    def listen(self):
        log("Waiting for request...")

        while True:
            data, (reqAddr, reqPort) = self.socket.recvfrom(4096)
            packet = RequestFactory.requestfrombytes(data, self.node._id)
            packet.handle(self, reqAddr, reqPort)

    def ping(self, address, port):
        ping = Ping(self.node._id)
        ping.send(self, address, port)

    def pong(self, address, port):
        pong = Pong(self.node._id)
        pong.send(self, address, port)

    def local_find_node(self, nodeid, port):
        localfindnode = LocalFindNode()
        localfindnode.setnodeid(nodeid)
        localfindnode.send(self, port)

    def getsocket(self):
        return self.socket
