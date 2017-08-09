import socket
import argparse
import select
import sys
from random import randrange

#define constants
g = 2
p = 0x00cc81ea8157352a9e9a318aac4e33ffba80fc8da3373fb44895109e4c3ff6cedcc55c02228fccbd551a504feb4346d2aef47053311ceaba95f6c540b967b9409e9f0502e598cfc71327c5a455e2e807bede1e0b7d23fbea054b951ca964eaecae7ba842ba1fc6818c453bf19eb9c5c86e723e69a210d4b72561cab97b3fb3060b
a = None
b = None
A = None
B = None

#enter the parser
parser = argparse.ArgumentParser(description="HW1 program")  #define parser equal to the library? I think
parser.add_argument('--s', dest='s', help='s takes no argument', action='store_true')   #add command line arguments
parser.add_argument('--c', dest='c', help='c takes one arg - type alice-md1341')       #for bob to connect to alice
args = parser.parse_args()  #defines args to contain the arguments just added

args = parser.parse_args()          #for testing - nothing should be printed
#print args
#print args.s
#print args.c

#FIGURE OUT IF CLIENT OR SERVER
if args.s:
    #SET UP SOCKET
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setblocking(0) #what does this mean??
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 9999))
    s.listen(10) #what does the number mean?
    conn, addr = s.accept()
    #server setup is complete

else:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect to the server
    conn.connect( (args.c,9999) )
    connected = True

if args.c:
    #client begins Diffie-Helman key exchange
    a = randrange(1, p)
    A = pow(g, a, p)
    conn.send(str(A) + '\n')

# server receives A, selects and sends b
if args.s:
    b = randrange(1, p)
    B = pow(g, b, p)
    conn.send(str(B) + '\n')

while True:
    L = [sys.stdin, conn]
    r,_,_ = select.select(L,[],[])

    #r can be sys.stdin or conn or both - use ifs to capture
    #these different options

    #server computes K
    if args.s:
        data = conn.recv(1024)
        A = int(data)

        #server computes K
        K = pow(A, b, p)
        print K

    # client receives B and computes K
    if args.c:
        data = conn.recv(1024)
        B = int(data)
        K = pow(B, a, p)
        print K

    """
    if sys.stdin in r:
        data = raw_input()
        conn.send(data)
        sys.stdout.flush()

    if conn in r:
        data = conn.recv(1024)
        print data
    """

#while loop does not end, but this is the end of the code in
#the while loop
