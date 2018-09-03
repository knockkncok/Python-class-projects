# -*- coding: utf-8 -*-
"""
Created on Tue May 22 16:12:17 2018

@author: test
"""
import socket
client=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
host=socket.gethostname()
port=9999
client.connect((host,port))
while True:
    print(client.recv(1024))