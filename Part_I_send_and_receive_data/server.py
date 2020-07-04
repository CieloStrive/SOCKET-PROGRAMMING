#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# AF_INET refers to IPv4, SOCK_STREAM refers to TCP


s.bind((socket.gethostname(),1234))
# bind the socket(an end point receive the data: IP + port)
# s.bind((IP,4-digits port number))

s.listen(5)
# Enable a server to accept connections. If backlog is specified, 
# it must be at least 0 (if it is lower, it is set to 0); 
# it specifies the number of unaccepted connections that the system will allow before refusing new connections. 
# If not specified, a default reasonable value is chosen.

while True:
    clientsocket, address = s.accept()
    # client socket object like s at top
    # address is address like IP

    print(f"connection from {address} has been established!")
    # a debugging print

    clientsocket.send(bytes("welcome to the server!","utf-8"))
    #send info to client by client object we get

    clientsocket.close()
    #close connection
    #if we don't close connection, it will stuck here
    #will not get into nexr loop