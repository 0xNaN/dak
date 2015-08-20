# DAK

usage: dak.py [-h] [-p PORT] [--to TO] [--listen] [--ping]
              [--local-find-node NODE_ID]

a simple Kademlia implementation

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  specify the port to use
  --to TO               specify the destination of a request. e.g:
                        <address>:<port>, <port>
  --listen              keep up the peer to listen incoming requests
  --ping                perform a PING request on the target peer
  --local-find-node NODE_ID
                        perform a FIND-NODE request on a local peer

**This is an experimental PoC with a lot of bug and stupid things**
