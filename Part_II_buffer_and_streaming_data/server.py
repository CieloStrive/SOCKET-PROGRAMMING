#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time

# how to keep program runing and know length of coming data
# use header

HEADERSIZE = 10

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"connection from {address} has been established!")

    msg = "Welcome to the server!"
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    #     use :< to do left alignment in header:
    #     result:
    #     "len(msg)_________msg"
    #      |   HEADERSIZE  |
    clientsocket.send(bytes(msg,"utf-8"))

    while True:
        time.sleep(3)
        msg = f"The time is {time.time()}"
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        clientsocket.send(bytes(msg,"utf-8"))


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



