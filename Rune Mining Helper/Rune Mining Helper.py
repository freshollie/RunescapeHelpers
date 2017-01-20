try:from tkinter import *
except ImportError: from Tkinter import *
import time


class World(object):
    def __init__(self,number,master,pos):
        self.root=master
        self.status=0 #0:Not Determined
                      #1:Mined
                      #2:Unmined
        self.number="World "+str(number)
        self.labelText=StringVar()
        self.button=Button(master,textvariable=self.labelText,command=self.doCommand,width=10,height=2,font=("Purisa", 7))
        self.button.grid(row = pos[1], column = pos[0])
        self.root.after(200,self.tick)

    def doCommand(self):
        self.setStatus(1)
        self.tick()
        
    def tick(self):
        if self.status==0:
            self.labelText.set(self.number+":\n Undetermined")
            self.button.configure(bg="white")
        elif self.status==1:
            if self.getTimeLeft()<1:
                self.setStatus(2)
                self.labelText.set(self.number+":\n Unmined")
                self.button.configure(bg="green")
            elif self.getTimeLeft()<60:
                self.labelText.set(self.number+":\n Mined: %ss" %(self.getTimeLeft()))
                self.button.configure(bg="orange")
            else:
                self.labelText.set(self.number+":\n Mined: %ss" %(self.getTimeLeft()))
                self.button.configure(bg="red")
        else:
            self.labelText.set(self.number+":\n Unmined")
            self.button.configure(bg="green")
        self.root.after(500,self.tick)

    def setStatus(self,status):
        self.status=status
        if status==1:
            self.timeMined=time.time()
        else:
            self.timeMined=None

    def getTimeLeft(self):
        return round(1002-(time.time()-self.timeMined))
    

class RuneMiner:
    def __init__(self,master):
        self.root=master
        self.root.wm_title("Ore Timer")
        image=PhotoImage(file='rune.gif')
        self.image=Label(master=self.root,image=image)
        self.image.grid(columnspan = 8, row = 0, column =0)
        self.root.resizable(0,0)
        self.running=True
        self.resetWorlds()
        self.root.mainloop()
        

    def resetWorlds(self):
        self.worlds=[]
        width=8
        col=0
        row=1
        for i in range(1,140):
            self.worlds.append(World(i,self.root,[col,row]))
            
            col+=1
            if col==width:
                row+=1
                col=0

RuneMiner(Tk())

    

