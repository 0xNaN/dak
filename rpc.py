from request import RemoteRequest, LocalRequest
from utils import log

class Ping(RemoteRequest):
    def __init__(self, nodeid):
        super().__init__(nodeid)

    def onreceive(self, peer, reqaddr, reqport):
        # respond with a Pong with the same communication's identifier
        pong = Pong(peer.node._id)
        pong.setidentifier(self.getidentifier())
        pong.send(peer, reqaddr, reqport)


class Pong(RemoteRequest):
    def __init__(self, nodeid):
        super().__init__(nodeid)


class LocalFindNode(LocalRequest):
    def __init__(self):
        super().__init__()

    def onreceive(self, peer, reqaddr, reqport):
        log('Searched nodeid: {}, result:'.format(self.getparam('searchedid')))
        for contact in peer.node.find_node(self.getparam('searchedid')):
            print(contact)

    def setnodeid(self, searchedid):
        self.addparam("searchedid", searchedid)
