# -*- coding: utf-8 -*-
"""
Created on Wed May 02 19:16:01 2018

@author: test
"""
import tkinter as tk
import random
import time

#Generate the number for the blocks randomly
def generate(map):
    random.seed(time.time())
    while True:
        r,c=random.randint(0,3),random.randint(0,3)
        if map[r][c]==0:
            n=random.randint(0,9)
            if n!=0:
                map[r][c]=2
                break
            else:
                map[r][c]=4
                break
    return map
#count the points of the game
def count_points(map):
    max=0
    for a in range(4):
        for b in range(4):
            if map[a][b]>max:
                max=map[a][b]
    if max<128:
        return 0
    elif max==128:
        return 5
    elif max==256:
        return 10
    elif max==512:
        return 20
    elif max==1024:
        return 30
    else:
        return 40
#check whether the gmae is over and print the points
def gameover_check(map2):
    if valid_move(map2,"Left") or valid_move(map2,"Right") or valid_move(map2,"Up") or valid_move(map2,"Down"):
        return False
    return True
#check whether the move is valid
def valid_move(map2,move):
    if move=="Left":
        for a in range(4):
            for b in reversed(range(1,4)):
                if map2[a][b]!=0 and (map2[a][b-1]==0 or map2[a][b]==map2[a][b-1]):
                    return True
        return False
    if move=="Right":
        for a in range(4):
            for b in range(0,3):
                if map2[a][b]!=0 and (map2[a][b+1]==0 or map2[a][b]==map2[a][b+1]):
                    return True
        return False
    if move=="Up":
        for b in range(4):
            for a in range(1,4):
                if map2[a][b]!=0 and (map2[a-1][b]==0 or map2[a][b]==map2[a-1][b]):
                    return True
        return False
    if move=="Down":
        for b in range(4):
            for a in range(0,3):
                if map2[a][b]!=0 and (map2[a+1][b]==0 or map2[a+1][b]==map2[a][b]):
                    return True
        return False
#decide how the boxes move and merge
def move_merge(map2,move):
    if move=="Left":
        for a in range(4):
            for b in range(1,4):
                c=b
                while c-1>=0 and map2[a][c-1]==0:
                    map2[a][c-1]=map2[a][c]
                    map2[a][c]=0
                    c-=1                   
        for a in range(4):
            for b in range(1,4):
                if map2[a][b]==map2[a][b-1]:
                    map2[a][b-1]*=2
                    map2[a][b]=0
        for a in range(4):
            for b in range(1,4):
                c=b
                while c-1>=0 and map2[a][c-1]==0:
                    map2[a][c-1]=map2[a][c]
                    map2[a][c]=0
                    c-=1
    if move=="Right":
        for a in range(4):
            for b in reversed(range(0,3)):
                c=b
                while c+1<=3 and map2[a][c+1]==0:
                    map2[a][c+1]=map2[a][c]
                    map2[a][c]=0
                    c+=1
        for a in range(4):
            for b in reversed(range(0,3)):
                if map2[a][b]==map2[a][b+1]:
                    map2[a][b+1]*=2
                    map2[a][b]=0
        for a in range(4):
            for b in reversed(range(0,3)):
                c=b
                while c+1<=3 and map2[a][c+1]==0:
                    map2[a][c+1]=map2[a][c]
                    map2[a][c]=0
                    c+=1
    if move=="Up":
        for b in range(4):
            for a in range(1,4):
                c=a
                while c-1>=0 and map2[c-1][b]==0:
                    map2[c-1][b]=map2[c][b]
                    map2[c][b]=0
                    c-=1
        for b in range(4):
            for a in range(1,4):
                if map2[a-1][b]==map2[a][b]:
                    map2[a-1][b]*=2
                    map2[a][b]=0
        for b in range(4):
            for a in range(1,4):
                c=a
                while c-1>=0 and map2[c-1][b]==0:
                    map2[c-1][b]=map2[c][b]
                    map2[c][b]=0
                    c-=1                    
    if move=="Down":
        for b in range(4):
            for a in reversed(range(0,3)):
                c=a
                while c+1<=3 and map2[c+1][b]==0:
                    map2[c+1][b]=map2[c][b]
                    map2[c][b]=0
                    c+=1
        for b in range(4):
            for a in reversed(range(0,3)):
                if map2[a+1][b]==map2[a][b]:
                    map2[a+1][b]*=2
                    map2[a][b]=0
        for b in range(4):
            for a in reversed(range(0,3)):
                c=a
                while c+1<=3 and map2[c+1][b]==0:
                    map2[c+1][b]=map2[c][b]
                    map2[c][b]=0
                    c+=1
#get the move of the user and decide how to move
def getmove(key,map1,map2,boxes):
    if key.keysym=="BackSpace":
        ok=False
        if map1[0][0]!=1:
            ok=True
        if ok:
            for a in range(4):
                for b in range(4):
                    map2[a][b]=map1[a][b]
            present(boxes,map2)
        else:
            pop_up=tk.Toplevel()
            warning=tk.Label(pop_up,text="Your move is invalid!")
            warning.pack()
    if key.keysym=="Left":
        if valid_move(map2,"Left"):
            for a in range(4):
                for b in range(4):
                    map1[a][b]=map2[a][b]
            move_merge(map2,"Left")
            generate(map2)
            present(boxes,map2)
            if gameover_check(map2):
                scorewindow=tk.Toplevel()
                scorelabel=tk.Label(scorewindow,text="Your score:"+str(count_points(map2)))
                scorelabel.pack()        
        else:
            pop_up=tk.Toplevel()
            warning=tk.Label(pop_up,text="Your move is invalid!")
            warning.pack()
    if key.keysym=="Right":
        if valid_move(map2,"Right"):
            for a in range(4):
                for b in range(4):
                    map1[a][b]=map2[a][b]
            move_merge(map2,"Right")
            generate(map2)
            present(boxes,map2)
            if gameover_check(map2):
                scorewindow=tk.Toplevel()
                scorelabel=tk.Label(scorewindow,text="Your score:"+str(count_points(map2)))
                scorelabel.pack()
        else:
            pop_up=tk.Toplevel()
            warning=tk.Label(pop_up,text="Your move is invalid!")
            warning.pack()
    if key.keysym=="Up":
        if valid_move(map2,"Up"):
            for a in range(4):
                for b in range(4):
                    map1[a][b]=map2[a][b]
            move_merge(map2,"Up")
            generate(map2)
            present(boxes,map2)
            if gameover_check(map2):
                scorewindow=tk.Toplevel()
                scorelabel=tk.Label(scorewindow,text="Your score:"+str(count_points(map2)))
                scorelabel.pack()
        else:
            pop_up=tk.Toplevel()
            warning=tk.Label(pop_up,text="Your move is invalid!")
            warning.pack()
    if key.keysym=="Down":
        if valid_move(map2,"Down"):
            for a in range(4):
                for b in range(4):
                    map1[a][b]=map2[a][b]
            move_merge(map2,"Down")
            generate(map2)
            present(boxes,map2)
            if gameover_check(map2):
                scorewindow=tk.Toplevel()
                scorelabel=tk.Label(scorewindow,text="Your score:"+str(count_points(map2)))
                scorelabel.pack()
        else:
            pop_up=tk.Toplevel()
            warning=tk.Label(pop_up,text="Your move is invalid!")
            warning.pack()
#connnect the map to the display and decide their color
def present(boxes,map2):
    for a in range(4):
        for b in range(4):
            if map2[a][b]!=0:
                boxes[a][b]['text']=map2[a][b]
                if boxes[a][b]['text']==2:
                    boxes[a][b]['bg']="cyan"
                elif boxes[a][b]['text']==4:
                    boxes[a][b]['bg']="deep sky blue"
                elif boxes[a][b]['text']==8:
                    boxes[a][b]['bg']="lawn green"
                elif boxes[a][b]['text']==16:
                    boxes[a][b]['bg']="lemon chiffon" 
                elif boxes[a][b]['text']==32:
                    boxes[a][b]['bg']="dark orange"
                elif boxes[a][b]['text']==64:
                    boxes[a][b]['bg']="red2"
                elif boxes[a][b]['text']==128:
                    boxes[a][b]['bg']="deep pink2"
                elif boxes[a][b]['text']==256:
                    boxes[a][b]['bg']="darkslategray1"
                elif boxes[a][b]['text']==512:
                    boxes[a][b]['bg']="green"
                elif boxes[a][b]['text']==1024:
                    boxes[a][b]['bg']="gold"
                else:
                    boxes[a][b]['bg']="yellow2"                    
            else:
                boxes[a][b]['text']=""
                boxes[a][b]['bg']="azure"
                
#initialize a game
def game2048():
    window=tk.Tk()
    map1,map2=[[0 for a in range(4)]for b in range(4)],[[0 for a in range(4)]for b in range(4)]
    map1[0][0]=1
    boxes=[[tk.Button(window,height=10,width=20) for a in range(4)]for b in range(4)] 
    for a in range(4):
        for b in range(4):
            boxes[a][b].grid(row=a,column=b)
    generate(map2)
    present(boxes,map2)
    window.bind("<Key>",lambda key:getmove(key,map1,map2,boxes))  
    window.mainloop()
#get the move from AI and decide how to move    
def getmoveforAI(key,map1,map2,boxes):
    if key=="Left":
        if valid_move(map2,"Left"):
            for a in range(4):
                for b in range(4):
                    map1[a][b]=map2[a][b]
            move_merge(map2,"Left")
            generate(map2)
            present(boxes,map2)
            if gameover_check(map2):
                scorewindow=tk.Toplevel()
                scorelabel=tk.Label(scorewindow,text="Your score:"+str(count_points(map2)))
                scorelabel.pack()        
        else:
            pop_up=tk.Toplevel()
            warning=tk.Label(pop_up,text="Your move is invalid!")
            warning.pack()
    if key=="Right":
        if valid_move(map2,"Right"):
            for a in range(4):
                for b in range(4):
                    map1[a][b]=map2[a][b]
            move_merge(map2,"Right")
            generate(map2)
            present(boxes,map2)
            if gameover_check(map2):
                scorewindow=tk.Toplevel()
                scorelabel=tk.Label(scorewindow,text="Your score:"+str(count_points(map2)))
                scorelabel.pack()
        else:
            pop_up=tk.Toplevel()
            warning=tk.Label(pop_up,text="Your move is invalid!")
            warning.pack()
    if key=="Up":
        if valid_move(map2,"Up"):
            for a in range(4):
                for b in range(4):
                    map1[a][b]=map2[a][b]
            move_merge(map2,"Up")
            generate(map2)
            present(boxes,map2)
            if gameover_check(map2):
                scorewindow=tk.Toplevel()
                scorelabel=tk.Label(scorewindow,text="Your score:"+str(count_points(map2)))
                scorelabel.pack()
        else:
            pop_up=tk.Toplevel()
            warning=tk.Label(pop_up,text="Your move is invalid!")
            warning.pack()
    if key=="Down":
        if valid_move(map2,"Down"):
            for a in range(4):
                for b in range(4):
                    map1[a][b]=map2[a][b]
            move_merge(map2,"Down")
            generate(map2)
            present(boxes,map2)
            if gameover_check(map2):
                scorewindow=tk.Toplevel()
                scorelabel=tk.Label(scorewindow,text="Your score:"+str(count_points(map2)))
                scorelabel.pack()
        else:
            pop_up=tk.Toplevel()
            warning=tk.Label(pop_up,text="Your move is invalid!")
            warning.pack()
#In order for the move of the computer to be seen every 0.5 seconds, a function
#that calls itself must be applied(time.sleep() would not work for tkinter. Hence, while loop cannot be
#used either.)
def AImovement(window,map1,map2,boxes):
    if not gameover_check(map2):
        if valid_move(map2,"Down"):
            getmoveforAI("Down",map1,map2,boxes)
        elif valid_move(map2,"Right"):
            getmoveforAI("Right",map1,map2,boxes)
        elif valid_move(map2,"Left"):
            getmoveforAI("Left",map1,map2,boxes)
        else:
            getmoveforAI("Up",map1,map2,boxes)
        window.after(500,lambda:AImovement(window,map1,map2,boxes))
#Computer that plays the game
def AI():
    window=tk.Tk()
    map1,map2=[[0 for a in range(4)]for b in range(4)],[[0 for a in range(4)]for b in range(4)]
    map1[0][0]=1
    boxes=[[tk.Button(window,height=10,width=20) for a in range(4)]for b in range(4)] 
    for a in range(4):
        for b in range(4):
            boxes[a][b].grid(row=a,column=b)
    generate(map2)
    present(boxes,map2)
    AImovement(window,map1,map2,boxes)
    window.mainloop()
if __name__ =='__main__':
    #computer plays the game
    #'''
    #AI()
    #'''
    #Game for the user to play
    game2048()
        