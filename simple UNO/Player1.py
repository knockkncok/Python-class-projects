# -*- coding: utf-8 -*-
"""
Created on Thu May 24 19:31:11 2018

@author: test
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 24 09:40:26 2018

@author: test
"""

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
    try:
        with open("c1.txt",'r') as f:
            del mycards[:]
            for line in f:
                if not len(line.strip())==0:
                    print(line)
                    mycards.append(card(line.split()[0],line.split()[1]))
    except:
        print("Can't open c1.txt")

def recommend_card():
    global mycards
    add_card=[]
    try:
        with open("c1.txt",'r') as f:
            del mycards[:]
            for line in f:
                if not len(line.strip())==0:
                    #line = line.strip('\n')
                    mycards.append(card(line.split()[0],line.split()[1]))
    except:
        print("Can't open c1.txt")
    try:
        with open("now.txt",'r') as f:
            t=f.readline()
            #t=t.strip('\n')
        no_card=True
        color=t.split()[0]
        represent=t.split()[1]
        for c in mycards:
            if c.color==color or c.represent=="Change" or c.represent==represent:
                print(c.color+" "+c.represent)
                no_card=False
        if no_card:
            with open("d3.txt",'r') as f:
                for line in f:
                    if not len(line.strip())==0:
                        add_card.append(card(line.split()[0],line.split()[1]))
            t=add_card.pop()
            mycards.append(t)
            with open("c1.txt",'w') as f:
                for c in mycards:
                    f.write(c.color+" "+c.represent+"\n")
            with open("d3.txt",'w') as f:
                for c in add_card:
                    f.write(c.color+" "+c.represent+"\n")
                
    except:
        print("Error happened!")
def read_current():
    try:
        with open("now.txt",'r') as f:
            print(f.readline())
    except:
        print("Can't open now.txt")
def send_card(turn):
    global mycards
    try:
        with open("c1.txt",'r') as f:
            del mycards[:]
            for line in f:
                if not len(line.strip())==0:
                    #line = line.strip('\n')
                    mycards.append(card(line.split()[0],line.split()[1]))
    except:
        print("Can't open c1.txt")
    if turn==2:
        print("It's not your turn yet!")
        return turn
    client.send("send_card")
    turn+=1
    with open("now.txt",'r') as f:
        t=f.readline()
    a=True
    while a:
        #print mycards[0].color+"    "+mycards[0].represent
        color=raw_input("Enter the color of the card:")
        represent=raw_input("Enter the represent of the card:")
        for c in mycards:
            if c.color==color and c.represent==represent:
                if t.split()[0]==color or t.split()[1]==represent or color=="All":
                    mycards.remove(c)
                    a=False
                    break
        if a:
            print("The card you enter is invalid. Please enter another card:")
    if color=="All":
        while True:
            color=raw_input("Enter the color that you want to change to:")
            if color not in ["B","G","R","Y"]:
                print("The color you want to change does not exist. Please enter another one!")
            else:
                break
    client.send(color+" "+represent)
    if represent=="Plus2":
        with open("c2.txt",'a') as fo:
            for a in range(2):
                fo.write(colors[random.randint(0,3)]+" "+str(random.randint(1,5))+"\n")
    with open("c1.txt",'w') as f:
        for c in mycards:
            f.write(c.color+" "+c.represent+"\n")
    return turn
def handle_server():
    global client,turn
    while True:
        try:
            msg=client.recv(1024)
            if msg.endswith("Your turn!"):
                turn-=1
                print(msg) 
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
        if command=="read_current":
            read_current()
        if command=="recommend_card":
            recommend_card()
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

