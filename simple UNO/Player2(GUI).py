# -*- coding: utf-8 -*-
"""
Created on Sat May 26 20:42:17 2018

@author: test
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:37:51 2018

@author: test
"""

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
import Tkinter as tk
class card():
    def __init__(self,color,represent):
        self.color=color
        self.represent=represent
def see_mycard():
    global mycards
    try:
        with open("c2.txt",'r') as f:
            del mycards[:]
            display.delete(0,tk.END)
            display.insert(tk.END,"My card:")
            for line in f:
                if not len(line.strip())==0:
                    display.insert(tk.END,line)
                    mycards.append(card(line.split()[0],line.split()[1]))
    except:
        print("Can't open c2.txt")

def recommend_card():
    global mycards
    add_card=[]
    if turn==1:
        display.delete(0,tk.END)
        display.insert(tk.END,"It's not your turn yet!")
        #print("It's not your turn yet!")
        return 
    try:
        with open("c2.txt",'r') as f:
            del mycards[:]
            for line in f:
                if not len(line.strip())==0:
                    #line = line.strip('\n')
                    mycards.append(card(line.split()[0],line.split()[1]))
    except:
        print("Can't open c2.txt")
    try:
        with open("now.txt",'r') as f:
            t=f.readline()
            #t=t.strip('\n')
        no_card=True
        color=t.split()[0]
        represent=t.split()[1]
        display.insert(tk.END,"Recommended cards:")
        for c in mycards:
            if c.color==color or c.represent=="Change" or c.represent==represent:
                display.insert(tk.END,c.color+" "+c.represent)
                no_card=False
        if no_card:
            with open("d3.txt",'r') as f:
                for line in f:
                    if not len(line.strip())==0:
                        add_card.append(card(line.split()[0],line.split()[1]))
            t=add_card.pop()
            display.insert(tk.END,"You have no card. Add card!")
            mycards.append(t)
            with open("c2.txt",'w') as f:
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
            display.delete(0,tk.END)
            display.insert(tk.END,"Current card:")
            display.insert(tk.END,f.readline())
    except:
        print("Can't open now.txt")
def send_card():
    if turn==1:
        display.delete(0,tk.END)
        display.insert(tk.END,"It's not your turn yet!")
        #print("It's not your turn yet!")
        return 
    color=input_color.get()
    represent=input_represent.get()
    color2=input_change.get()
    global mycards,turn
    try:
        with open("c2.txt",'r') as f:
            del mycards[:]
            for line in f:
                if not len(line.strip())==0:
                    #line = line.strip('\n')
                    mycards.append(card(line.split()[0],line.split()[1]))
    except:
        print("Can't open c2.txt")
    

    with open("now.txt",'r') as f:
        t=f.readline()
    a=True

    for c in mycards:
        if c.color==color and c.represent==represent:
            if t.split()[0]==color or t.split()[1]==represent or color=="All":
                if color=="All":
                    if color2 not in ["B","G","R","Y"]:
                        display.insert(tk.END,"The color you want to change does not exist.\nPlease enter another one!")
                        #print("The color you want to change does not exist. Please enter another one!")
                        return
                    else:
                        color=color2
                mycards.remove(c)
                a=False
    if a:
        display.insert(tk.END,"The card you enter is invalid.\nPlease enter another card:")
        #print("The card you enter is invalid. Please enter another card:")
        return
    client.send("send_card")
    client.send(color+" "+represent)
    if represent=="Plus2":
        with open("c1.txt",'a') as fo:
            for a in range(2):
                fo.write(colors[random.randint(0,3)]+" "+str(random.randint(1,5))+"\n")
    with open("c2.txt",'w') as f:
        for c in mycards:
            f.write(c.color+" "+c.represent+"\n")
    turn-=1
    return
def handle_server():
    global client,turn
    while True:
        try:
            msg=client.recv(1024)
            if msg.endswith("Your turn!"):
                turn+=1
                display.insert(tk.END,msg)
                #print(msg) 
            elif msg.endswith("wins"):
                display.insert(tk.END,msg)
                break
            elif msg.endswith("\0"):
                msg=msg.replace("\0","")
                display.insert(tk.END,msg)
            else:
                display.insert(tk.END,msg)
                #print(msg) 
        except:
            break
client=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
host=socket.gethostname()
port=9999
mycards=[]
client.connect((host,port))
turn=1
colors=["B","G","R","Y"]
if __name__ =='__main__':
    accept_thread=Thread(target=handle_server)
    accept_thread.start()
    window=tk.Tk()
    window.title("Player 2") 
    window.geometry("1024x768") #You want the size of the app to be 1024x768
    window.resizable(0,0) #不想讓使用者調整視窗大小
    f1=tk.Frame()
    f2=tk.Frame()
    f3=tk.Frame()
    
    #f1 (function button part)
    #send_c=tk.Button(f1,text="Send card",command=send_card).pack()
    recommend_c=tk.Button(f1,text="Recommend card",height=5,width=20,command=recommend_card).pack()
    see_c=tk.Button(f1,text="See my cards",height=5,width=20,command=see_mycard).pack()
    read_c=tk.Button(f1,text="Read current card",height=5,width=20,command=read_current).pack()
    
    #f2 (Send card part)  #done~~~~~
    l1=tk.Label(f2,text="Enter the color of the card(B,G,R,Y,All):").grid(row=0,column=0,sticky='wens')
    l2=tk.Label(f2,text="Enter the number of the card(1~5,Plus2,Change):").grid(row=1,column=0,sticky='wens')
    l3=tk.Label(f2,text="Enter the color to change to(B,G,R,Y):").grid(row=2,column=0,sticky='wens')
    input_color=tk.Entry(f2,width=20)
    input_represent=tk.Entry(f2,width=20)
    input_change=tk.Entry(f2,width=20)
    enter_button=tk.Button(f2,text="Send card",height=5,width=20,command=send_card).grid(row=1,column=2,sticky='we')
    input_color.grid(row=0,column=1,ipady=30,sticky='wens')
    input_represent.grid(row=1,column=1,ipady=30,sticky='wens')
    input_change.grid(row=2,column=1,ipady=30,sticky='wens')
    #f3 (show console part)
    display=tk.Listbox(f3,height=20,width=50)
    displaysb=tk.Scrollbar(f3,orient='vertical',command=display.yview)
    display.config(yscrollcommand=displaysb.set)
    display.grid(row=0,column=0)
    displaysb.grid(row=0,column=1,sticky='we')
    
    f1.grid(column=0)
    f2.grid(row=0,column=1)
    f3.grid(row=1,column=1)
    
    
    window.mainloop()
    accept_thread.join()
    client.close()

