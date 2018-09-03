# -*- coding: utf-8 -*-
"""
Created on Tue May 22 16:08:27 2018

@author: test
"""
import socket
server=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)         
host=socket.gethostname() 
port=9999            
server.bind((host, port))
server.listen(5)
client, client_address =server.accept()
while True:
   
    print("Client has connected.")
    client.send("Hello world!")