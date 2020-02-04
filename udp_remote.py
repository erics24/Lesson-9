#!/usr/bin/env python3

import argparse, random, sys, time
from socket import *

MAX_BYTES = 65535

def server(interface, port):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES) 
        text = data.decode('ascii')
        print('The client at {} says {}'.format(address, text))
        message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'), address)
        
## Students modify the client function to request user input and send to the server.
def client(hostname, port):
    sock = socket(AF_INET, SOCK_DGRAM)
    print(sock)
    message_count = 1
    print('Client socket name is {}'.format(sock.getsockname())) ## initial IP/port assignment    
    
    while True:
        text = "This is message # " + str(message_count)
        data = text.encode('ascii')
        sock.sendto(data, (hostname, port))
        print('New socket name is {}'.format(sock.getsockname())) ## after first transmission IP/port assignment    
    
        message_count += 1
        response = sock.recv(MAX_BYTES)
        time.sleep(2)
        print('The server says {}'.format(response.decode('ascii')))

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                     ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
