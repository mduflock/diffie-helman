import socket
import argparse
import select
import sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
import binascii

#enter the parser
parser = argparse.ArgumentParser(description="HW1 program")  #define parser equal to the library? I think
parser.add_argument('--s', dest='s', help='s takes no argument', action='store_true')   #add command line arguments
parser.add_argument('--c', dest='c', help='c takes one arg - type alice-md1341')       #for bob to connect to alice
parser.add_argument('--genkey', dest ='genkey', help='genkey takes no argument', action='store_true')
    #to determine which option to use
parser.add_argument('--m', dest='m', help='m takes one argument - the message')   #to type in messages or genkey

args = parser.parse_args()  #defines args to contain the arguments just added

args = parser.parse_args()          #for testing - nothing should be printed
#print args
#print args.s
#print args.c

def mypad(some_num):
    return '0' * (4 - len(str(some_num))) + str(some_num)

#determine which mode is selected
if args.genkey:
    #generate keypair - 4096 bits
    key = RSA.generate(4096)
    #passes back an rsa_obj with a public key and private key function
    #use the export function to store the private key in myprivkey.pem
    file = open('myprivkey.pem','w')
    file.write(key.exportKey('PEM'))
    file.close()
    #stores prive key in directory called myprivkey.pem

    #use the public key export function
    file = open('mypubkey.pem','w')
    file.write(key.publickey().exportKey('PEM'))
    file.close()
    #stores public key in directory called mypubkey.pem

"""
#for testing - be the server
if args.s:
    #SET UP SOCKET
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setblocking(0) #what does this mean??
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 9998))
    s.listen(10) #what does the number mean?
    conn, addr = s.accept()
    #server setup is complete
"""

if args.c:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect to the server
    conn.connect( (args.c,9998) )
    connected = True

    #send SIGNED VERSION of message - access myprivkey.pem
    message = args.m
    key = RSA.importKey(open('myprivkey.pem').read())
    h = SHA256.new(message)
    signer = PKCS1_v1_5.new(key)
    signature = binascii.hexlify(signer.sign(h))
    conn.send( (mypad(len(message))) + message + mypad(len(signature)) + signature )

"""
# only receive while the server
if args.s is not None:
    # this is all server - purely for testing
    message_len = int(conn.recv(4, socket.MSG_WAITALL))
    message = conn.recv(message_len, socket.MSG_WAITALL)
    signature_len = int(conn.recv(4, socket.MSG_WAITALL))
    signature_hexed = conn.recv(signature_len, socket.MSG_WAITALL)
    signature = binascii.unhexlify(signature_hexed)

    #pubkey_pem = key.publickey().exportKey()
    key = RSA.importKey(open('mypubkey.pem').read())
    h = SHA256.new(message)
    verifier = PKCS1_v1_5.new(key)

    if verifier.verify(h, signature):
        print "The signature is authentic."
    else:
        print "The signature is not authentic."
"""