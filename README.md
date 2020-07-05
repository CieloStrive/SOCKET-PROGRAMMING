# SOCKET-PROGRAMMING

---

- [SOCKET-PROGRAMMING](#socket-programming)
  - [Part I: sending and receving data](#part-i-sending-and-receving-data)
    - [1. create server](#1-create-server)
    - [2. create client](#2-create-client)
    - [3. Test connection](#3-test-connection)
    - [4. explore the buffer](#4-explore-the-buffer)
  - [Part II: buffer and streaming data](#part-ii-buffer-and-streaming-data)
    - [1. build a server sending message with header](#1-build-a-server-sending-message-with-header)
    - [2. build a client that can sparse header](#2-build-a-client-that-can-sparse-header)
    - [3. run and check output](#3-run-and-check-output)
    - [4. send time](#4-send-time)
  - [Part III: sending and receving python objects with *Pickle*](#part-iii-sending-and-receving-python-objects-with-pickle)
    - [1. import pickle](#1-import-pickle)
    - [2. create server](#2-create-server)
    - [3. create client](#3-create-client)
    - [4. check output](#4-check-output)
  - [Part IV: build a socket chat room](#part-iv-build-a-socket-chat-room)
    - [1. build the server](#1-build-the-server)
    - [2. build the client](#2-build-the-client)
    - [3. check output](#3-check-output)

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

---

## Part III: sending and receving python objects with *Pickle*

### 1. import pickle

Python pickle module is used for serializing and de-serializing a Python object structure. Any object in Python can be pickled so that it can be saved on disk. What pickle does is that it “serializes” the object first before writing it to file. Pickling is a way to convert a python object (list, dict, etc.) into a character stream. The idea is that this character stream contains all the information necessary to reconstruct the object in another python script.

### 2. create server

```py
import socket
import time
import pickle

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
```

### 3. create client

```py
import socket
import pickle

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
```

### 4. check output

![](/images/2020-07-02-14-43-41.png)


---

## Part IV: build a socket chat room

**\*** *details can be dound in another repository specifically for the thread version of this part*

### 1. build the server


```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import select
# give OS level IO ability no matter WIN/MAC/LINUX
# select() 函数是部署底层操作系统的直接接口。
# 它监视着套接字，打开的文件和管道（任何调用 fileno() 方法后会返回有效文件描述符的东西）直到它们变得可读可写或有错误发生。
# select() 让我们同时监视多个连接变得简单，同时比在 Python 中使用套接字超时写轮询池要有效，
# 因为这些监视发生在操作系统网络层而不是在解释器层。



HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234


server_socket =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
# without waiting for its natural timeout to expire.
# SOL-Socket Option Level, SO-Socket Option, 1 is true, allows us to reconnect

server_socket.bind((IP,PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {} #用户空字典，记录用户


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except: #一般不会
        return False



while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    # select.select(rlist, wlist, xlist[, timeout])
    # This is a straightforward interface to the Unix select() system call.
    # The first three arguments are iterables of ‘waitable objects’:
    # either integers representing file descriptors or objects with a parameterless method named fileno() returning such an integer:

    # rlist: wait until ready for reading
    # wlist: wait until ready for writing
    # xlist: wait for an “exceptional condition” (see the manual page for what your system considers such a condition)

    for notified_socket in read_sockets:
        #read_sockets是select监听的sockets_list里的可读套接字，并且它此时有数据可读！（用户申请加入群组或用户发来消息）
        #如果该可读套接字是主服务器，对它的处理是让他准备好接受新的连接
        if notified_socket == server_socket: #means some one just wamt to connect to this server: new user
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)#第一次发来的信息是用户信息
            if user is False:
                continue

            #将新的套接字加如监听列表
            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Accept new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket)

            if message is False: #用户退群
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket] #通过用户字典对应此时的用户
            print(f"receive message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket: #发送给群组里面的其他用户
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
```

### 2. build the client

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

#create an username
my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP,PORT))

client_socket.setblocking(False)
#set connection to non-blocking state, so .recv() call won't block, just return some exception we will handle

#first connect to server sending your username
username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)


while True: #发现一个缺陷，更新消息会被input阻塞，按回车更新
    message = input(f"{my_username} > ")

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

    #receive message
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)

            #if we receive no data from server(receive header but no message), close connection
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        # This is normal on non-blocking connections -- when there are no incoming data, error will be raised
        # some OS will indicate that using AGAIN, and some using WOULDBLOCK
        # we gonna check both, if one of tht two hit, just continue
        # if hit none of this two, something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error',str(e))
            sys.exit()
        continue   #if it is E AGAIN or E WOULD BLOCK, we don't care, continue

    except Exception as e:
        # ANy other exception happened, exit
        print('General error',str(e))
        sys.exit()
```

### 3. check output

**conclusion**:

an drawback: input will block message to be updated, must type enter or send new message. We can fix this by threads.
发现一个缺陷，更新消息会被input阻塞，按回车或者输入信息才会更新，可使用threads解决

**server**:

![](/images/2020-07-03-16-53-38.png)

**client**:

![](/images/2020-07-03-16-54-42.png)

![](/images/2020-07-03-16-54-57.png)