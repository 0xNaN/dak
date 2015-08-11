import hashlib
import random

from utils import log

class PacketFactory():
     def packetfrombytes(rawPacket, nodeId):
        reqType, reqIdentifier, reqNodeId = [row.decode() for row in rawPacket.split(b'\n')]

        if(reqType == 'Ping'):
            p = Ping(reqNodeId)
        elif(reqType == 'Pong'):
            p = Pong(reqNodeId)
        else:
            p = Packet(reqNodeId)

        p.setreceiverid (nodeId)
        p.setidentifier(reqIdentifier)
        return p

class Packet:
    def __init__(self, nodeid):
        self.identifier = hashlib.sha256(str(random.randint(0, 2**32 - 1)).encode('utf-8')).hexdigest()[:20]
        self.senderid = nodeid
        self.receiverid = None

        self.typename = type(self).__name__

    def send(self, peer, address, port):
        log("Sending {} to {}:{}".format(self.typename, address, port))
        # header:
        #    PACKET_TYPE    (e.g: Ping, Pong, ...)
        #    COMMUNICATION_ID
        #    SENDER_NODE_ID
        #
        packet = "{}\n{}\n{}".format(self.typename, self.identifier, self.senderid).encode('utf-8')
        packet += self.getraw()

        socket = peer.getsocket()
        socket.sendto(packet, (address, port))

    def setidentifier(self, identifier):
        self.identifier = identifier

    def onreceive(self, peer, reqaddr, reqport):
        log("received an unknown packet")

    def getraw(self):
        return b''

    def setreceiverid(self, nodeid):
        self.receiverid = nodeid

    def __str__(self):
        return "{}\n{}\n{}".format(self.typename, self.identifier, self.senderid)

class Ping(Packet):
    def __init__(self, nodeid):
        super(self.__class__, self).__init__(nodeid)

    def onreceive(self, peer, reqaddr, reqport):
        log('Received a Ping from {}:{} aka {}'.format(reqaddr, reqport, self.senderid))
        print(self)

        # respond with a Pong with the same communication's identifier
        pong = Pong(self.receiverid)
        pong.setidentifier(self.identifier)
        pong.send(peer, reqaddr, reqport)

class Pong(Packet):
    def __init__(self, nodeid):
        super(self.__class__, self).__init__(nodeid)
        self._nodeid = nodeid

    def onreceive(self, peer, reqaddr, reqport):
        log('received a Pong from {}:{}'.format(reqaddr, reqport))
        print(self)
