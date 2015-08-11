#!/bin/env python3

import random
import argparse
import socket
import hashlib

from utils import log
from peer import Peer
from node import Node

def main():
    parser = argparse.ArgumentParser(description='a simple Kademlia implementation')
    parser.add_argument('-j', '--join')
    parser.add_argument('-p', '--port')
    parser.add_argument('--ping')

    args = parser.parse_args()

    node = Node(20)
    port = random.randint(2000, 8000) if args.port == None else int(args.port)
    peer = Peer(node, port)

    log('Peer started at {}'.format(port))
    log('Node id {}'.format(node.getid()))

    if(args.ping != None):
        toAddr, toPort = args.ping.split(':')
        toPort = int(toPort)
        peer.ping(toAddr, toPort)
    elif(args.join != None):
        toAddr, toPort = args.join.split(':')
        toPort = int(toPort)
        log('Joining to {}:{}'.format(toAddr, toPort))
        peer.join(toAddr, toPort)

    peer.listen()

if __name__ == '__main__':
    main()
