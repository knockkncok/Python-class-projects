# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:45:41 2018

@author: test
"""
import socket
import random
from threading import Thread
class card():
    def __init__(self,color,represent):
        self.color=color
        self.represent=represent
def see_mycard():
    global mycards
    with open("c1.txt",'r') as f:
        del mycards[:]
        for line in f:
            if not len(line.strip())==0:
                #line = line.strip('\n')
                print line
                mycards.append(card(line.split()[0],line.split()[1]))
'''
def read_current():
    global client
    print "Hello"
    client.send("read_current")
    data=client.recv(1024)
    print "Hello"
    print data
    try:
        with open("now.txt",'w') as f:
            f.write(data)
    except Exception as e:
        print e
    print "Hello"
'''
def recommend_card():
    global mycards
    try:
        with open("c1.txt",'r') as f:
            del mycards[:]
            for line in f:
                if not len(line.strip())==0:
                    #line = line.strip('\n')
                    mycards.append(card(line.split()[0],line.split()[1]))
    except:
        pass
    try:
        with open("s_now.txt",'r') as f:
            t=f.readline()
            #t=t.strip('\n')
            color=t.split()[0]
            represent=t.split()[1]
            for c in mycards:
                if c.color==color:
                    print(c.color+" "+c.represent)
                elif c.represent==represent or c.represent=="Change Color":
                    print(c.color+" "+c.represent)
    except:
        pass
def send_card(turn):
    global mycards
    client.send("send_card")
    if turn==2:
        print("It's not your turn yet!")
        return turn
    turn+=1
    a=True
    while a:
        print mycards[0].color+"    "+mycards[0].represent
        color=raw_input("Enter the color of the card:")
        represent=raw_input("Enter the represent of the card:")
        for c in mycards:
            if c.color==color and c.represent==represent:
                mycards.remove(c)
                a=False
                break
        if a:
            print("You don't have the card you enter. Please enter another card:")
    client.send(color+" "+represent)
    if represent=="Plus2":
        with open("c2.txt",'a') as fo:
            for a in range(2):
                fo.write(colors[random.randint(0,3)]+" "+str(random.randint(1,5)))
    with open("c1.txt",'w') as f:
        for c in mycards:
            f.write(c.color+" "+c.represent+"\n")
    return turn
def handle_server():
    global client,turn
    while True:
        try:
            msg=client.recv(1024)
            if msg=="turn":
                turn-=1
            else:
                print(msg) 
        except:
            break
def SimUNO():
    global turn
    accept_thread=Thread(target=handle_server)
    accept_thread.start()
    while True:
        command=raw_input("Please enter command(Quit to leave):")
        if command=="Quit":
            break
        if command=="send_card":
            turn=send_card(turn)
        if command=="recommend_card":
            recommend_card()
        if command=="read_current":
            read_current()
        if command=="see_mycard":
            see_mycard()
    accept_thread.join()

client=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
host=socket.gethostname()
port=9999
mycards=[]
client.connect((host,port))
turn=1
colors=["B","G","R","Y"]
if __name__ =='__main__':
    SimUNO()
    client.close()

