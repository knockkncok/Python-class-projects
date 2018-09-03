# -*- coding: utf-8 -*-
"""
Created on Tue May 15 20:14:16 2018

@author: test
"""
import socket
import random
from threading import Thread
import os
class card():
    def __init__(self,color,represent):
        self.color=color
        self.represent=represent
def generate_card():
    colors=["B","G","R","Y"]
    cards=[]
    for a in colors:
        for b in range(1,6):
            cards.append(card(a,str(b)))
        for b in range(2):
            cards.append(card(a,"Plus2"))
    for b in range(2):
        cards.append(card("All","Change Color"))
    random.shuffle(cards)
    with open("data.txt",'w') as f:
        for a in cards:
            #print(a.color+" "+a.represent)
            f.write(a.color+" "+a.represent+"\n")
def div_card():
    cards=[]
    with open("data.txt",'r') as f:
        for line in f:
            line = line.strip('\n')
            cards.append(card(line.split()[0],line.split()[1]))
    with open("d1.txt",'w') as f1, open("d2.txt",'w') as f2, open("d3.txt",'w') as f3:
        for a in range(5):
            f1.write(cards[a].color+" "+cards[a].represent+"\n")
        for a in range(5,10):
            f2.write(cards[a].color+" "+cards[a].represent+"\n")
        for a in range(10,30):
            f3.write(cards[a].color+" "+cards[a].represent+"\n")
    colors=["B","G","R","Y"]
    with open("now.txt",'w') as f4,open("s_now.txt",'w') as f5:
        a=card(str(random.randint(1,5)),colors[random.randint(0,3)])
        f4.write(a.color+" "+a.represent+"\n")
        f5.write(a.color+" "+a.represent+"\n")
def accepting_clients():
    a=1
    while True:
        client, client_address =server.accept()
        print("Client"+str(a)+" has connected.")
        clients[a]=client
        a+=1
        Thread(target=handle_client, args=(client,)).start()

def send_card():
    for a in clients:
        #print str(clients)
        #clients[a].send("Checking whether send or not"+str(a))
        with open("d"+str(a)+".txt",'r') as f1, open("c"+str(a)+".txt",'w') as f2:
            for line in f1:
                if not len(line.strip())==0:
                    #line = line.strip('\n')
                    print line
                    clients[a].send(line)  
                    f2.write(line+"\n")
def rec_card(client):
    try:
        with open("now.txt",'r') as f1:
            data=f1.readline()
            print("Recieved:"+data)
    except:
        pass
    with open("s_now.txt",'w') as f:
        f.write(data)
    for a in clients:
        clients[a].send("Current card is:"+data)
        if client!=clients[a]:
            clients[a].send("turn")
            
def check_game_state():
    if os.stat("c1.txt").st_size==0:
        return "Player1 wins!"
    if os.stat("c2.txt").st_size==0:
        return "Player2 wins!"
    if os.stat("d3.txt").st_size==0:
        return "Tie!"
    return "" #empty string is false 
def handle_client(client):
    global previous_player
    while True:
        msg=client.recv(1024)
        if msg=="read_current":
            with open("s_now.txt",'r') as f:
                print"OK"
                line=f.readline()
                print ("T:"+line)
                print"P"
                #client.send("Current card is:")#+line)
                print"OK"
                client.send("Current card is:shit")
                client.send("Why 2 times?")
        if msg=="send_card":
            print("Recieved card:"+client.recv(1024))
            previous_player=client
def SimUNO():
    server.listen(5)
    accept_thread=Thread(target=accepting_clients)
    accept_thread.start()
    while True:
        command=raw_input("Please enter command(Quit to leave):")
        if command=="Quit":
            break
        if command=="generate_card":
            generate_card()
        if command=="div_card":
            div_card()
        if command=="send_card":
            send_card()
        if command=="rec_card":
            rec_card(previous_player)   
    accept_thread.join()
    server.close()
    
server=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)         
host=socket.gethostname() 
port=9999            
server.bind((host, port))
clients={}
previous_player=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
if __name__ =='__main__':
    with open("s_now.txt",'w' ):
        pass
    with open("now.txt",'w' ):
        pass
    SimUNO()