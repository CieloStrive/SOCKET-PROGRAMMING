#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time
import pickle

# Python pickle module is used for serializing and de-serializing a Python object structure. 
# Any object in Python can be pickled so that it can be saved on disk. 
# What pickle does is that it “serializes” the object first before writing it to file. 
# Pickling is a way to convert a python object (list, dict, etc.) into a character stream. 
# The idea is that this character stream contains all the information necessary to reconstruct the object in another python script.


HEADERSIZE = 10

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"connection from {address} has been established!")

    d = {1: "Hey", 2: "There"}
    msg = pickle.dumps(d)
    # this is already bytes,so we need to transfer header to bytes in msg

    msg = bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8") + msg
    # now msg is already bytes

    clientsocket.send(msg)

    # while True:
    #     time.sleep(3)
    #     msg = f"The time is {time.time()}"
    #     msg = f'{len(msg):<{HEADERSIZE}}' + msg
    #     clientsocket.send(bytes(msg,"utf-8"))


    #clientsocket.close()


#
# Aligning the text and specifying a width:
#
# >>> '{:<30}'.format('left aligned')
# 'left aligned                  '
# >>> '{:>30}'.format('right aligned')
# '                 right aligned'
# >>> '{:^30}'.format('centered')
# '           centered           '
# >>> '{:*^30}'.format('centered')  # use '*' as a fill char
# '***********centered***********'



