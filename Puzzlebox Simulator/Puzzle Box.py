try:from tkinter import *
except:from Tkinter import *
import random
import time
import datetime
import os
from PIL import Image,ImageTk


class Tile:
    def __init__(self,master,moveFunction,pos,num,im,crop):
        self.im=ImageTk.PhotoImage(im.crop(crop))
        self.tiles=[]
        self.im.width=50
        self.root=master
        self.num=num
        self.pos=pos
        self.moveFunction=moveFunction
        self.button=Button(master=master, command=self.move, width=49, height=49,image=self.im)
        self.setPos(pos)

    def move(self):
        self.root.after(200,self.moveFunction, self)

    def setPos(self,pos):
        self.pos=pos[:]
        self.button.grid(column=pos[0], row=pos[1])

    def getPos(self):
        return self.pos[:]


class PuzzleBox:
    def __init__(self):
        self.root=Tk()
        self.root.title("Freshollie's rs puzzle practice")
        self.root.resizable(0,0)
        self.lastPuzzle=None
        self.puzzleNum=random.choice(range(len(os.listdir("puzzles/"))))
        self.timeLabel=StringVar()
        self.timeLabel.set("0:00:00")
        self.title=Label(master=self.root,textvariable=self.timeLabel)
        self.title.grid(row=0,column=0)
        self.scrambleButton=Button(master=self.root, text="Scramble",command=self.scramble)
        self.scrambleButton.grid(row=0,column=1)
        self.newPuzzleButton=Button(master=self.root, text="New Puzzle",command=self.newPuzzle)
        self.newPuzzleButton.grid(row=0,column=2)
        self.newPuzzle()
        self.root.after(1,self.tick)
        self.root.mainloop()

    def getPuzzle(self):
        puzzles=os.listdir("puzzles/")
        self.puzzleNum+=1
        if self.puzzleNum>=len(puzzles):
            self.puzzleNum=0
        puzzle=puzzles[self.puzzleNum]
        image=Image.open("puzzles/"+puzzle)
        return image

    def destoryOldPuzzle(self):
        for tile in self.tiles:
            tile.destroy()
        self.frame.destroy()

    def newPuzzle(self):
        self.tiles=[]
        self.frame=Frame(self.root,width=300,height=300)
        self.frame.grid(row=1,column=0,columnspan=3)
        self.emptyCell=[4,4]
        self.image=self.getPuzzle()
        self.started=False
        self.startTime=None
        
        num=1
        for i in range(5):
            for j in range(5):
                crop=self.getCropFromPos([j,i])
                self.tiles.append(Tile(self.frame,self.doMove,[j,i],num,self.image,crop))
                num+=1
        self.tiles[-1].button.destroy()
        del self.tiles[-1]

    def isComplete(self):
        num=0
        for i in range(5):
            for j in range(5):
                if num==24:
                    return True
                if self.tiles[num].getPos()[1]!= i or self.tiles[num].getPos()[0]!=j:
                    return False
                num+=1
        return True
        

    def getCropFromPos(self,pos):
        borderWidth=16
        borderHeight=13
        
        width=49
        space=7

        col=pos[0]
        row=pos[1]

        co1=borderWidth+(col*space)+(col*width)
        co2=borderHeight+(row*space)+(row*width)

        co3=co1+width
        co4=co2+width

        return (co1,co2,co3,co4)

    def checkMove(self,pos):
        if [pos[0],pos[1]-1]==self.emptyCell:
            return True
        elif [pos[0]-1,pos[1]]==self.emptyCell:
            return True
        elif [pos[0]+1,pos[1]]==self.emptyCell:
            return True
        elif [pos[0],pos[1]+1]==self.emptyCell:
            return True
        else:
            return False

    def doMove(self,tile,isScramble=False):
        pos = tile.getPos()
        if self.checkMove(pos):
            if not isScramble and not self.started:
                self.started=True
                self.startTime=time.time()
            tile.setPos(self.emptyCell)
            self.emptyCell=pos[:]

    def scramble(self):
        self.started=False
        self.startTime=None
        for i in range(1000):
            while True:
                tile = random.choice(self.tiles)
                if self.checkMove(tile.getPos()):
                    self.doMove(tile,True)
                    break

    def tick(self):
        if self.started:
            if self.isComplete():
                self.started=False
            else:
                self.timeLabel.set(str(datetime.timedelta(seconds=(time.time()-self.startTime))))
        self.root.after(1,self.tick)
            
PuzzleBox()
    


        
        
