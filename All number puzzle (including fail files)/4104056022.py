import Tkinter as tk
import Queue
from threading import Thread,Event
import random
class board():
  def __init__(self,now,previous,steps=None):
      self.now=now
      self.previous=previous  
      self.steps=steps
class pop_up(tk.Toplevel):
    def __init__(self,movements,r1,c1,r,c):
        tk.Toplevel.__init__(self)
        self.movements=list(movements)
        t=[[0 for a in range(3)]for b in range(3)]
        for a in range(3):
            for b in range(3):
                t[a][b]=movements[len(movements)-1].now[a][b]
        t[r][c]=t[r1][c1]
        t[r1][c1]=0
        self.movements.append(board(t,movements[len(movements)-1]))
        self.f1=tk.Frame(self)
        self.numbers=[[tk.Button(self.f1,height=10,width=20,bg='lavender') for a in range(3)]for b in range(3)]
        for a in range(3):
            for b in range(3):
                self.numbers[a][b].grid(row=a,column=b)
        self.f2=tk.Frame(self)
        self.step_label=tk.Label(self.f2,text='Number of steps: '+str(len(self.movements)-1))
        self.step_label.pack()
        self.f1.grid(row=0,column=0)
        self.f2.grid(row=0,column=1)
    
def play(numbers,movements,step_label):
   movements[:]=[]
   dic={1:[[1,7,8],[5,0,2],[4,3,6]],2:[[3,1,4],[5,0,6],[8,7,2]],3:[[4,7,1],[3,0,5],[8,2,6]]}
   movements.append(board(dic[random.randint(1,3)],None))
   for a in range(3):
       for b in range(3):
           numbers[a][b]['text']=""
   present(numbers,movements[0])
   step_label['text']=('Number of steps: 0')
def present(numbers,board):
   for a in range(3):
       for b in range(3):
           if board.now[a][b]!=0:
               if a==0 and board.now[a][b]==b+1:
                   numbers[a][b]['bg']='lawn green'
               elif a==1 and board.now[a][b]==b+4:
                   numbers[a][b]['bg']='lawn green'
               elif a==2 and board.now[a][b]==b+7:
                   numbers[a][b]['bg']='lawn green'
               else:
                   numbers[a][b]['bg']='lavender'
               numbers[a][b]['text']=board.now[a][b]
           else:
               numbers[a][b]['bg']='lavender'
               numbers[a][b]['text']=""
def move(numbers,number,movements,step_label):
   if len(movements)==0 or number=="":
       return
   row,col=getindex(movements[len(movements)-1],number)
   leave=False
   for a in range(row-1,row+2):
       for b in range(col-1,col+2):
           if a>=0 and a<3 and b>=0 and b<3 and abs(a-row)+abs(b-col)==1:
               if movements[len(movements)-1].now[a][b]==0 :
                   leave=True
                   t=[[0 for c in range(3)]for d in range(3)] 
                   for c in range(3):
                       for d in range(3):
                           t[c][d]=movements[len(movements)-1].now[c][d]
                   t[a][b]=t[row][col]
                   t[row][col]=0
                   break
       if leave:
           break
   if not leave:
       return
   movements.append(board(t,movements[len(movements)-1]))
   present(numbers,movements[len(movements)-1])
   step_label['text']=('Number of steps: '+str(len(movements)-1))
def getindex(board,number):
   for a in board.now:
       for b in a:
           if number==b:
               return board.now.index(a),board.now[board.now.index(a)].index(b)
def Return(numbers,movements,step_label):
    if len(movements)<=1:
        return
    movements.pop()
    present(numbers,movements[len(movements)-1])
    step_label['text']=('Number of steps: '+str(len(movements)-1))
def check_game_state(numbers):
    correct=0
    for a in range(3):
        for b in range(3):
            if numbers[a][b]['bg']=='lawn green':
                correct+=1
    if correct==8:
        return True
    return False
def count_points(numbers):
    correct=0
    for a in range(3):
        for b in range(3):
            if numbers[a][b]['bg']=='lawn green':
                correct+=1
    if correct<=3:
        return correct*10
    else:
        return (correct-3)*5+30
def multithread(movements,pop_ups):
    if len(movements)==0:
        return
    for a in pop_ups:
        a.destroy()
    pop_ups[:]=[]
    r,c=getindex(movements[len(movements)-1],0)
    for a in range(3):
        for b in range(3):
            if abs(a-r)+abs(c-b)==1:
                pop_ups.append(pop_up(movements,a,b,r,c))
    for a in pop_ups:
        present(a.numbers,a.movements[len(a.movements)-1])
def AI(pop_ups,stop_thread,finish):
    finish.clear()
    if len(pop_ups)==0:
        return
    solutions=Queue.Queue()
    t=[]
    for pop_up in pop_ups:
        t.append(Thread(target=solution_finding,args=(pop_up.movements[len(pop_up.movements)-1],solutions,)))     
    for tt in t:
        tt.start()
    for tt in t:
        tt.join()
        print "F2"
    t=[]
    for pop_up in pop_ups:
        t.append(Thread(target=AIprint,args=(pop_up,len(pop_up.movements),solutions.get(),stop_thread,finish,)))
    for tt in t:
        print "F3"
        tt.start()
    '''
    for tt in t:
        tt.join()
    '''
def AIprint(pop_up,step_number,solution,stop_thread,finish):
    if len(pop_up.movements)==201:
        pop_up.step_label['text']='Number of steps: '+str(step_number-1)+"\n"+str(count_points(pop_up.numbers))+" points."
        return
    if check_game_state(pop_up.numbers):
        finish.set()
    if finish.is_set():
        pop_up.step_label['text']='Number of steps: '+str(step_number-1)+"\n"+str(count_points(pop_up.numbers))+" points."
        return
    if stop_thread.is_set():
        pop_up.after(1000,lambda:AIprint(pop_up,step_number,solution,stop_thread,finish))
        return
    if len(solution)==0:
        return
    present(pop_up.numbers,solution.pop())
    pop_up.step_label['text']='Number of steps: '+str(step_number)
    pop_up.after(1000,lambda:AIprint(pop_up,step_number+1,solution,stop_thread,finish))
def solution_finding(current_board,solutions):
    current_board.steps=0
    current_board.previous=None
    nextmoves=[]
    target=[[1,2,3],[4,5,6],[7,8,0]]
    possible_path=Queue.PriorityQueue() 
    been_through=[]
    been_through.append(current_board.now)
    pre=current_board
    while(not list_same(target,pre.now)):   
        r,c=getindex(pre,0)
        for a in range(3):
            for b in range(3):
                if abs(a-r)+abs(c-b)==1:
                    t=[[0 for z in range(3)]for x in range(3)]
                    for z in range(3):
                        for x in range(3):
                            t[z][x]=pre.now[z][x]
                    t[r][c]=t[a][b]
                    t[a][b]=0
                    if t not in been_through:
                        been_through.append(t)
                        possible_path.put((priority_count2(t,pre,target,possible_path),board(t,pre,pre.steps+1)))
        pre=possible_path.get()[1]
    nextmoves.append(pre)
    while pre.previous!=None:
        pre=pre.previous 
        nextmoves.append(pre)
    nextmoves.reverse()
    nextmoves[:]=nextmoves[1:]
    nextmoves.reverse()
    solutions.put(nextmoves)
def priority_count2(t,pre,target,possible_path):
    z=0
    for x in t:
        for xx in x:        
            for a in range(3):
                for b in range(3):
                    if xx==target[a][b]:
                        z+=abs(t.index(x)-a)+abs(t[t.index(x)].index(xx)-b)
    return z+pre.steps
def list_same(l1,l2):
    for a in range(3):
        for b in range(3):
            if l1[a][b]!=l2[a][b]:
                return False
    return True
def stop(s):
    if not s.is_set():
        s.set() 
    else:
        s.clear()            
def number_puzzle():
  window=tk.Tk()
  movements=[]
  pop_ups=[]
  f1=tk.Frame()
  finish=Event()
  numbers=[[tk.Button(f1,height=10,width=20,bg='lavender') for a in range(3)]for b in range(3)]
  for a in range(3):
      for b in range(3):
          numbers[a][b]['command']=lambda a=a,b=b:move(numbers,numbers[a][b]['text'],movements,step_label)
          numbers[a][b].grid(row=a,column=b)
  f2=tk.Frame()
  play_button=tk.Button(f2,height=5,width=20,text='Play',command=lambda:play(numbers,movements,step_label))
  return_button=tk.Button(f2,height=5,width=20,text='Return',command=lambda:Return(numbers,movements,step_label))
  multithread_button=tk.Button(f2,height=5,width=20,text='Multithread',command=lambda:multithread(movements,pop_ups))
  AI_button=tk.Button(f2,height=5,width=20,text='AI',command=lambda:AI(pop_ups,stop_thread,finish))
  step_label=tk.Label(f2,text='Number of steps: '+str(len(movements)))
  step_label.pack()
  play_button.pack()
  return_button.pack()
  multithread_button.pack()
  AI_button.pack()
  f1.grid(row=0,column=0)
  f2.grid(row=0,column=1)
  stop_thread=Event()
  window.bind("<space>",lambda event:stop(stop_thread))  
  window.mainloop()

if __name__ =='__main__':
  number_puzzle()