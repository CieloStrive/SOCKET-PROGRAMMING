# SOCKET-PROGRAMMING

---

## Part I: sending and receving data

### 1. create server

*refer to server.py*

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# AF_INET refers to IPv4, SOCK_STREAM refers to TCP


s.bind((socket.gethostname(),1234))
# bind the socket(an end point receive the data: IP + port)
# s.bind((IP,4-digits port number))

s.listen(5)
#this is server, it is going to prepare for the incoming connection
#it leave a queue of 5
#if multiple connections come so fast

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

```

### 2. create client

*refer to client.py*

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((socket.gethostname(),1234))
#this is for local test

msg = s.recv(1024)
#how many chunks of data we want to receive at most for each time

print(msg.decode("utf-8"))
#print decoded message
```

### 3. Test connection

open two cmd for server and client

![](/images/2020-07-01-16-57-49.png)

![](/images/2020-07-01-16-58-44.png)

### 4. explore the buffer

1. let's try to make 1024 to 8

```py
msg = s.recv(8)
#how many chunks of data we want to receive for most at a time

print(msg.decode("utf-8"))
#print decoded message
```

* output:
![](/images/2020-07-01-17-14-14.png)


2. let's try smaller for several times

```py
#let's try smaller buffer for several time:
while True:
    msg = s.recv(8)
    print(msg.decode("utf-8"))
```

* output:
![](/images/2020-07-01-17-19-45.png)

3. do real streaming buffer work

```py
# 3. try simple real buffer work
full_msg = ''
while True:
    msg = s.recv(8)
    if len(msg) <= 0:
        break;
    full_msg += msg.decode("utf-8")
print(full_msg)
```

* output:
* ![](/images/2020-07-01-17-39-38.png)

---

## Part II: buffer and streaming data

### 1. build a server sending message with header

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

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
    #clientsocket.close()
    
```

Aligning the text and specifying a width in Python:

```
>>> '{:<30}'.format('left aligned')
'left aligned                  '
>>> '{:>30}'.format('right aligned')
'                 right aligned'
>>> '{:^30}'.format('centered')
'           centered           '
>>> '{:*^30}'.format('centered')  # use '*' as a fill char
'***********centered***********'
```

### 2. build a client that can sparse header

```py
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
```

### 3. run and check output

![](/images/2020-07-01-18-55-28.png)

### 4. send time 

1. `import time` and add sending time in `while` loop

```py
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
```

2. run cmd and check

![](/images/2020-07-01-19-03-22.png)


