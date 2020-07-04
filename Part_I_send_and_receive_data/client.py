#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((socket.gethostname(),1234))
#this is for local test

# 1. simply set data size received for one time very large
# msg = s.recv(1024)
# #how many chunks of data we want to receive at a time
#
# print(msg.decode("utf-8"))
# #print decoded message


# 2. let's try smaller buffer for several time:
# while True:
#     msg = s.recv(8)
#     print(msg.decode("utf-8"))

# 3. try simple real buffer work
full_msg = ''
while True:
    msg = s.recv(8)
    if len(msg) <= 0:
        break;
    full_msg += msg.decode("utf-8")
print(full_msg)
