import socket

from utils import log
from node import Node
from rpc import Ping, Pong, Request, RequestFactory, FindNode

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

            #update the bucket on every request
            reqType, reqIdentifier, reqNodeId, packetData = [row.decode() for row in data.split(b'\n')]
            contact = (reqNodeId, reqAddr, reqPort)
            self.node.addcontact(contact)

            packet.onreceive(self, reqAddr, reqPort)

    def ping(self, address, port):
        ping = Ping(self.node._id)
        ping.send(self, address, port)

    def pong(self, address, port):
        pong = Pong(self.node._id)
        pong.send(self, address, port)

    def find_node(self, nodeid, address, port):
        findnode = FindNode(self.node._id)
        findnode.setSearchedId(nodeid)
        findnode.send(self, address, port)

    def getsocket(self):
        return self.socket


