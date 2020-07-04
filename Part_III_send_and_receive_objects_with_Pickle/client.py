#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import pickle

# Python pickle module is used for serializing and de-serializing a Python object structure. 
# Any object in Python can be pickled so that it can be saved on disk. 
# What pickle does is that it “serializes” the object first before writing it to file. 
# Pickling is a way to convert a python object (list, dict, etc.) into a character stream. 
# The idea is that this character stream contains all the information necessary to reconstruct the object in another python script.

HEADERSIZE = 10

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((socket.gethostname(),1234))

while True:
    full_msg = b'' #full_msg should be bytes!
    new_msg = True

    while True:
        # receive a little bit more than the header size for each time
        msg = s.recv(16)
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        # assemble message with out any decoding
        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            print("full message received")
            print("objects received without decoding:")
            print(full_msg[HEADERSIZE:])
            #check what is here without decodeing

            d = pickle.loads(full_msg[HEADERSIZE:])
            print("decoded objects:")
            print(d)
            #now check what is print here

            new_msg = True
            full_msg = b''  #clear buffer for new message

    print(full_msg)

