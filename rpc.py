import hashlib
import random

from utils import log

class RequestFactory():
     def requestfrombytes(rawRequest, nodeId):
        reqType, reqIdentifier, reqNodeId, packetData = [row.decode() for row in rawRequest.split(b'\n')]

        if(reqType == 'Ping'):
            p = Ping(reqNodeId)
        elif(reqType == 'Pong'):
            p = Pong(reqNodeId)
        elif(reqType == 'FindNode'):
            p = FindNode(reqNodeId)
        else:
            p = Request(reqNodeId)

        p.setreceiverid (nodeId)
        p.setidentifier(reqIdentifier)
        p.addParamsFromString(packetData)
        return p

class Request:
    def __init__(self, nodeid):
        self.identifier = hashlib.sha256(str(random.randint(0, 2**32 - 1)).encode('utf-8')).hexdigest()[:20]
        self.senderid = nodeid
        self.receiverid = None
        self.typename = type(self).__name__
        self.params = {}

    def send(self, peer, address, port):
        log("Sending {} to {}:{}".format(self.typename, address, port))
        packet = "{}\n{}\n{}\n".format(self.typename, self.identifier, self.senderid).encode('utf-8')
        for param in self.params:
            packet += '{}={},'.format(param, self.params[param]).encode('utf-8')

        socket = peer.getsocket()
        socket.sendto(packet, (address, port))

    def setidentifier(self, identifier):
        self.identifier = identifier

    def onreceive(self, peer, reqaddr, reqport):
        log("received an unknown packet")

    def setreceiverid(self, nodeid):
        self.receiverid = nodeid

    def addparam(self, name, value):
        self.params[name] = value

    def addParamsFromString(self, params):
        for param in params.split(',')[:-1]:
            name, value = param.split('=')
            self.addparam(name, value)

    def __str__(self):
        return "{}\n{}\n{}\n{}".format(self.typename, self.identifier, self.senderid, str(self.params))

class Ping(Request):
    def __init__(self, nodeid):
        super(self.__class__, self).__init__(nodeid)

    def onreceive(self, peer, reqaddr, reqport):
        log('Received a Ping from {}:{} aka {}'.format(reqaddr, reqport, self.senderid))
        print(self)

        # respond with a Pong with the same communication's identifier
        pong = Pong(self.receiverid)
        pong.setidentifier(self.identifier)
        pong.send(peer, reqaddr, reqport)

class Pong(Request):
    def __init__(self, nodeid):
        super(self.__class__, self).__init__(nodeid)

    def onreceive(self, peer, reqaddr, reqport):
        log('received a Pong from {}:{}'.format(reqaddr, reqport))
        print(self)

class FindNode(Request):
    def __init__(self, nodeid):
        super(self.__class__, self).__init__(nodeid)

    def onreceive(self, peer, reqaddr, reqport):
        log('received a FindNode from {}:{}'.format(reqaddr, reqport))
        print(peer.node.find_node(self.params['searchedid']))

    def setSearchedId(self, searchedid):
        self.addparam("searchedid", searchedid)
