#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((socket.gethostname(),1234))

while True:
    full_msg = ''
    new_msg = True
    #set a flag to indicate if new message comes

    while True:
        msg = s.recv(16) #receive a little bit more than the header size for each time
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8") #assemble message

        if len(full_msg) - HEADERSIZE == msglen:
            print("full message received")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''  #clear buffer for new message

    print(full_msg)

