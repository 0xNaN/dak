#!/bin/env python3

import random
import argparse
import socket
import hashlib
import os

from utils import log
from peer import Peer
from node import Node

def main():
    parser = argparse.ArgumentParser(description='a simple Kademlia implementation')
    parser.add_argument('-p', '--port')
    parser.add_argument('--to')
    parser.add_argument('--ping', action = 'store_true')
    parser.add_argument('--find-node')
    parser.add_argument('--listen', action = 'store_true')

    args = parser.parse_args()

    node = Node(20)
    port = random.randint(2000, 8000) if args.port == None else int(args.port)
    peer = Peer(node, port)

    log('Peer started at {}'.format(port))
    log('Node id {}'.format(node.getid()))

    if(args.to != None):
        toAddr, toPort = args.to.split(':')
        toPort = int(toPort)

    if(args.ping and args.to != None):
        peer.ping(toAddr, toPort)

    if(args.find_node != None and args.to != None):
        peer.find_node(args.find_node, toAddr, toPort)

    if(args.listen):
        peer.listen()


if __name__ == '__main__':
    main()
