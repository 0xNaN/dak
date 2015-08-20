import hashlib
import random

from utils import log

class Request:
    """ creates a request intended to be sended/received from a peer.

    A request defines the following items:
        - the raw packet sent through the socket owned by a Peer
        - a request action to perform when received `onreceive()'

    The packet has the following structure:

        <PacketTypeName>                e.g:    Ping
        <PacketHeader>                          2a6a75094940ecbdc4ac
        <ParamName>=<ParamValue>,[...]          identifier=0c47561d45d2d6adc5a7,
    """

    def __init__(self):
        self._params = {}
        self._typename = type(self).__name__

    def send(self, peer, address, port):
        log("Sending {} to {}:{}".format(self._typename, address, port))
        packet = "{}\n{}\n".format(self._typename, self.header()).encode('utf-8')
        for param in self._params:
            packet += '{}={},'.format(param, self._params[param]).encode('utf-8')

        socket = peer.getsocket()
        socket.sendto(packet, (address, port))

    def handle(self, peer, reqaddr, reqport):
        log("Received an unknown packet")
        print(self)
        return self.onreceive(peer, reqaddr, reqport)

    def header(self):
        return ""

    def onreceive(self, peer, reqaddr, reqport):
        pass

    def addparam(self, name, value):
        self._params[name] = value

    def getparam(self, name):
        return  self._params[name]

    def addParamsFromString(self, params):
        for param in params.split(',')[:-1]:
            name, value = param.split('=')
            self.addparam(name, value)

    def __str__(self):
        return "{}\n{}".format(self._typename, str(self._params))


class LocalRequest(Request):
    """ creates a local request

    A Local Request is a Request sent from the same host that owns a peer.
    Is intended to be used for querying a Peer and not meet the same constraints
    found in request designed for Kademlia (RemoteRequest).
    """
    def __init__(self):
        super().__init__()

    def send(self, peer, port):
        super().send(peer, "", port)

    def handle(self, peer, reqaddr, reqport):
        if(reqaddr != "127.0.0.1"):
            raise Exception("LocalRequest from Remote Host")
        log("Received a {} from port {}".format(type(self).__name__, reqport))
        print(self)
        return self.onreceive(peer, reqaddr, reqport)


class RemoteRequest(Request):
    """ creates a request intended to be sent/received from another remote Peer

    A Remote Request is a Request sent from another Peer in the net.
    It contains Peer's informations that informs the receiver of its presence on the net on each request.
    """

    def __init__(self, senderid):
        super().__init__()
        self.senderid = senderid
        self.addparam("identifier", hashlib.sha256(str(random.randint(0, 2**32 - 1)).encode('utf-8')).hexdigest()[:20])

    def header(self):
        return self.getsenderid()

    def handle(self, peer, reqaddr, reqport):
        log('Received a {} from {}:{} aka {}'.format(type(self).__name__, reqaddr, reqport, self.getsenderid()))
        print(self)

        # Update the kbucket on each RemoteRequest
        contact = (self.getsenderid(), reqaddr, reqport)
        peer.node.addcontact(contact)
        return self.onreceive(peer, reqaddr, reqport)

    def setidentifier(self, identifier):
        self.addparam("identifier", identifier)

    def setreceiverid(self, nodeid):
        self.addparam("receiverid", nodeid);

    def setsenderid(self, nodeid):
        self.senderid = nodeid

    def getsenderid(self):
        return self.senderid

    def getidentifier(self):
        return self.getparam('identifier')


