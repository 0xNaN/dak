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
    parser.add_argument('-p', '--port', help = "specify the port to use")
    parser.add_argument('--to', help = "specify the destination of a request. e.g: <address>:<port>, <port>")
    parser.add_argument('--listen', action = 'store_true', help = "keep up the peer to listen incoming request")
    parser.add_argument('--ping', action = 'store_true', help = "perform a PING request on the target peer")
    parser.add_argument('--local-find-node', metavar = "NODE_ID", help = "perform a FIND-NODE request on a local peer")
    args = parser.parse_args()

    node = Node(20)
    port = random.randint(2000, 8000) if args.port == None else int(args.port)
    peer = Peer(node, port)

    log('Peer started at port {}'.format(port))
    log('Node id {}'.format(node.getid()))

    toAddr = ""
    if(args.to != None):
        if args.to.__contains__(':'):
            toAddr, toPort = args.to.split(":")
        else:
            toPort = args.to
        toPort = int(toPort)

    if(args.ping and args.to != None):
        peer.ping(toAddr, toPort)

    if(args.local_find_node != None and args.to != None):
        peer.local_find_node(args.local_find_node, toPort)

    if(args.listen):
        peer.listen()


if __name__ == '__main__':
    main()
