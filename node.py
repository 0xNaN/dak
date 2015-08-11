import hashlib
import random
from math import log2

from utils import log
from kbucket import KBucket

def xor(b1, b2):
    assert len(b1) == len(b2)
    return int.from_bytes(b1, 'big') ^ int.from_bytes(b2, 'big')

class Node:
    def __init__(self, k):
       self._id =  hashlib.sha256(str(random.randint(0, 2**32 - 1)).encode('utf-8')).hexdigest()[:20]
       self._kbucket = KBucket(k)

    def getid(self):
        return self._id

    def addcontact(self, contact):
        contactId = contact[0]

        distance = xor(self._id.encode('utf-8'), contactId.encode('utf-8'))
        if(log2(distance).__round__() - 1  <= log2(distance)):
            index = log2(distance).__round__() - 1
        else:
            index = log2(distance).__round__()
        log("addding {} to bucket {}".format(contactId, index))
        self._kbucket.add(contact, index)
