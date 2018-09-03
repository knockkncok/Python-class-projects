# -*- coding: utf-8 -*-
"""
Created on Sat May 26 21:00:37 2018

@author: test
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 24 09:28:21 2018

@author: test
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 15 20:14:16 2018

@author: test
"""
import socket
import random
from threading import Thread
import os
import Tkinter as tk
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
            display.insert(tk.END,a.color+" "+a.represent+"\n")
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
        a=card(colors[random.randint(0,3)],str(random.randint(1,5)),)
        f4.write(a.color+" "+a.represent+"\n")
        f5.write(a.color+" "+a.represent+"\n")
def accepting_clients():
    global display
    a=1
    while True:
        client, client_address =server.accept()
        display.insert(tk.END,"Client"+str(a)+" has connected.") # to insert the data
        #display.update_idletasks() # to update the GUI
        #print("Client"+str(a)+" has connected.")
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
                    display.insert(tk.END,line) # to insert the data
                    #display.update_idletasks() # to update the GUI
                    #display.insert(line)
                    #print line
                    clients[a].send(line+"\0")  
                    f2.write(line+"\n")            
def check_game_state():
    if os.stat("c1.txt").st_size==0:
        return "Player1 wins!"
    if os.stat("c2.txt").st_size==0:
        return "Player2 wins!"
    if os.stat("d3.txt").st_size==0:
        return "Tie!"
    return "" #empty string is false 
def handle_client(client):
    while True:
        msg=client.recv(1024)
        if msg=="send_card":
            data=client.recv(1024)
            display.insert(tk.END,"Recieved card:"+data) # to insert the data
            #display.update_idletasks() # to update the GUI
            #print("Recieved card:"+data)
            with open("now.txt",'w') as f1,open("s_now.txt",'w') as f2:
                f1.write(data+"\n")
                f2.write(data+"\n")      
            for a in clients:
                clients[a].send("(Read_current)")
                clients[a].send("Current card is:"+data+"\n")
                if clients[a]!=client:
                    clients[a].send("Your turn!")  
                if check_game_state():
                    clients[a].send(check_game_state())
            

    
    
server=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)         
host=socket.gethostname() 
port=9999            
server.bind((host, port))
clients={}
if __name__ =='__main__':
    server.listen(5)
    accept_thread=Thread(target=accepting_clients)

    accept_thread.start()
    window=tk.Tk()
    window.title("Server") 
    window.geometry("1024x768") #You want the size of the app to be 1024x768
    window.resizable(0,0) #不想讓使用者調整視窗大小
    f1=tk.Frame()
    f2=tk.Frame()
    
    generate_c=tk.Button(f1,text="Generate card",height=5,width=20,command=generate_card)
    div_c=tk.Button(f1,text="Divide card",height=5,width=20,command=div_card)
    send_c=tk.Button(f1,text="Send card",height=5,width=20,command=send_card)
    generate_c.pack()
    div_c.pack()
    send_c.pack()
    
    display=tk.Listbox(f2,height=20,width=50)
    displaysb=tk.Scrollbar(f2,orient='vertical',command=display.yview)
    display.config(yscrollcommand=displaysb.set)
    display.grid(row=0,column=0)
    displaysb.grid(row=0,column=1,sticky='we')
    
    f1.grid(row=0,column=0)
    f2.grid(row=0,column=1)
    window.mainloop()
    
    accept_thread.join()
    server.close()