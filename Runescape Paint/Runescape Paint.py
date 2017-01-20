try: from Tkinter import *
except: from tkinter import *
try: import messagebox
except: pass
import datetime
from Input import *
from urllib import request
import collections
import threading
import requests

rcEvalTask="self.rcFunc()" #Gaint Pouch breaks after 12 runs


def convertToRs(number):
    number=int(number)
    if number<100000:
        return number
    elif number<10000000:
        return str(number)[:-3]+"K"
    else:
        return str(number)[:-6]+"M"
        
        
        

class Paint:

    def __init__(self,listeningKey, priceOfItem, moneySpentPerRun, itemsPerRun, xpPerItem,task=None):
        constBG='darkgray'
        self.startTime=None
        font=(20)
        width=17
        self.root=Tk()
        self.root.configure(bg=constBG)
        self.root.title('Rs Paint')
        self.task=task
        self.bankingKey=listeningKey
        self.itemPrice=priceOfItem
        self.lossPerRun=moneySpentPerRun
        self.numItems=itemsPerRun
        self.xpPerItem=xpPerItem

        self.frame1=Frame(self.root,bg=constBG)
        self.frame1.grid(row=0,column=0,columnspan=3)
        
        self.frame2=Frame(self.root,bg=constBG)
        self.frame2.grid(row=1,column=0,columnspan=3)


        self.itemLabel=Label(self.frame1, text="GP/Item: %s" %(self.itemPrice),width=20,bg=constBG,font=font)
        self.itemLabel.grid(row=0,column=0)

        self.itemsPerRunLabel=Label(self.frame1, text="Items/Run: %s" %(self.numItems),width=20,bg=constBG,font=font)
        self.itemsPerRunLabel.grid(row=1,column=0)

        self.lossPerRunLabel=Label(self.frame1, text="Loss/Run: %s" %(self.lossPerRun),width=20,bg=constBG,font=font)
        self.lossPerRunLabel.grid(row=2,column=0)

        self.itemLabel=Label(self.frame1, text="Xp/Item: %s" %(self.xpPerItem),width=20,bg=constBG,font=font)
        self.itemLabel.grid(row=3,column=0)

        self.timeText=StringVar()
        self.timeLabel=Label(self.frame1, textvariable=self.timeText, width=18,bg=constBG,font=font)
        self.timeLabel.grid(row=0,column=1)

        self.currRunLengthText=StringVar()
        self.currRunLengthLabel=Label(self.frame1, textvariable=self.currRunLengthText, width=width,bg=constBG,font=font)
        self.currRunLengthLabel.grid(row=1,column=1)

        self.avgText=StringVar()
        self.avgLabel=Label(self.frame1, textvariable=self.avgText, width=width,bg=constBG,font=font)
        self.avgLabel.grid(row=2,column=1)

        self.fastestText=StringVar()
        self.fastestLabel=Label(self.frame1, textvariable=self.fastestText, width=30,bg=constBG,font=font)
        self.fastestLabel.grid(row=3,column=1)
        
        self.runsCompletedText=StringVar()
        self.runsCompletedLabel=Label(self.frame2, textvariable=self.runsCompletedText,width=width,bg=constBG,font=font)
        self.runsCompletedLabel.grid(row=0,column=2)

        self.xpGainedText=StringVar()
        self.xpGainedLabel=Label(self.frame2, textvariable=self.xpGainedText, width=width,bg=constBG,font=font)
        self.xpGainedLabel.grid(row=0,column=3)
        
        self.xpPerHourText=StringVar()
        self.xpPerHourLabel=Label(self.frame2, textvariable=self.xpPerHourText, width=width,bg=constBG,font=font)
        self.xpPerHourLabel.grid(row=1,column=3)

        self.itemsCollected=StringVar()
        self.itemsCollectedLabel=Label(self.frame2, textvariable=self.itemsCollected, width=width,bg=constBG,font=font)
        self.itemsCollectedLabel.grid(row=0,column=4)

        self.itemsPerHourText=StringVar()
        self.itemsPerHourLabel=Label(self.frame2, textvariable=self.itemsPerHourText, width=width,bg=constBG,font=font)
        self.itemsPerHourLabel.grid(row=1,column=4)

        self.moneyMadeText=StringVar()
        self.moneyMadeLabel=Label(self.frame2, textvariable=self.moneyMadeText, width=width,bg=constBG,font=font)
        self.moneyMadeLabel.grid(row=0,column=5)
        
        self.moneyPerHourText=StringVar()
        self.moneyPerHourLabel=Label(self.frame2, textvariable=self.moneyPerHourText, width=width,bg=constBG,font=font)
        self.moneyPerHourLabel.grid(row=1,column=5)

        self.allowedNewRun=True

        self.pausePlayText=StringVar()
        self.pausePlayText.set('Pause')

        self.paused=False
        
        self.pausePlay=Button(self.root, textvar=self.pausePlayText, command=self.pauseToggle)
        self.pausePlay.grid(row=4,column=0)

        self.resetButton=Button(self.root, text='Reset', command=self.reset)
        self.resetButton.grid(row=4,column=1)

        self.toggleLockButton=Button(self.root, text='Toggle Lock', command=self.toggleLock)
        self.toggleLockButton.grid(row=4,column=2)
        self.toggle=False

        self.root.bind('t',self.toggleLock)
        
        Input.bind(listeningKey,self.newRun)
        self.reset()

        self.root.after(10,self.tick)
        self.root.mainloop()

    def pauseToggle(self):
        if not self.startTime:
            return
        if self.paused:
            self.pausePlayText.set('Pause')
            self.startTime+=(time.time()-self.pauseTime)
            self.runTime+=(time.time()-self.pauseTime)
            self.paused=False
        else:
            self.pauseTime=time.time()
            self.paused=True
            self.pausePlayText.set('Play')

    def textToColour(self,text):
        if 'M' in str(text):
            return 'green'
        elif 'K' in str(text):
            return 'white'
        else:
            return 'yellow'
        
    def rcFunc(self):
        if not self.runsCompleted%12 and self.runsCompleted:
            self.xpGained-=self.xpPerItem*6
            self.numCollected-=6

    def getPerHour(self,number):
        if self.startTime:
            timeElapsed=time.time()-self.startTime
        else:
            return 0
        
        if timeElapsed==0:
            return 0

        rough=number/timeElapsed
        return round(rough*3600)

    def allowNewRun(self):
        self.allowedNewRun=True
        

    def updateText(self):
        if self.startTime:
            self.timeText.set("Running Time: %s" %(str(datetime.timedelta(seconds=round(time.time()-self.startTime)))))
        else:
            self.timeText.set("Running Time: %s" %(str(datetime.timedelta(0))))

        if self.runTime:
            self.currRunLengthText.set("This Run: %s" %(str(datetime.timedelta(seconds=round(time.time()-self.runTime)))))
        else:
            self.currRunLengthText.set("This Run: %s" %(str(datetime.timedelta(0))))

        if self.runsCompleted:
            self.avgText.set("Avg Length: %s" %(str(datetime.timedelta(seconds=round((time.time()-self.startTime)/self.runsCompleted)))))
        else:
            self.avgText.set("Avg Length: N/A")

        if self.fastestTime:
            self.fastestText.set("Fastest Run: %s" %(str(datetime.timedelta(seconds=self.fastestTime))))
        else:
            self.fastestText.set("Fastest Run: N/A")
            
        
        self.runsCompletedText.set("Runs Completed: %s" %(convertToRs(self.runsCompleted)))
        self.runsCompletedLabel.configure(fg=self.textToColour(convertToRs(self.runsCompleted)))
        
        self.xpGainedText.set("Xp: %s" %(convertToRs(self.xpGained)))
        self.xpGainedLabel.configure(fg=self.textToColour(convertToRs(self.xpGained)))
        
        self.xpPerHourText.set("Xp/H: %s" %(convertToRs(self.getPerHour(self.xpGained))))
        self.xpPerHourLabel.configure(fg=self.textToColour(convertToRs(self.getPerHour(self.xpGained))))

        self.itemsCollected.set("Items: %s" %(convertToRs(self.numCollected)))
        self.itemsCollectedLabel.configure(fg=self.textToColour(convertToRs(self.numCollected)))

        self.itemsPerHourText.set("Items/H: %s" %(convertToRs(self.getPerHour(self.numCollected))))
        self.itemsPerHourLabel.configure(fg=self.textToColour(convertToRs(self.getPerHour(self.numCollected))))

        self.moneyMadeText.set("Money Made: %s" %(convertToRs(self.moneyMade)))
        self.moneyMadeLabel.configure(fg=self.textToColour(convertToRs(self.moneyMade)))

        self.moneyPerHourText.set("Money/H: %s" %(convertToRs(self.getPerHour(self.moneyMade))))
        self.moneyPerHourLabel.configure(fg=self.textToColour(convertToRs(self.getPerHour(self.moneyMade))))

        
        

    def newRun(self):
        if self.paused:
            return 
        self.allowedNewRun=False
        
        if not self.startTime:
            self.startTime=time.time()
            self.runTime=time.time()
            self.root.after(3000,self.allowNewRun)
            return
        
        fastestTime=time.time()-self.runTime
        if self.fastestTime:
            if fastestTime<self.fastestTime:
                self.fastestTime=fastestTime
        else:
            self.fastestTime=fastestTime
            
        self.runTime=time.time()
        
        if self.task:
            eval(self.task)
            
        self.runsCompleted+=1
        
        self.numCollected+=self.numItems
        self.xpGained+=self.numItems*self.xpPerItem
        self.moneyMade=((self.numCollected*self.itemPrice)-(self.runsCompleted*self.lossPerRun))
        self.root.after(3000,self.allowNewRun)

    def reset(self):
        if self.paused:
            self.pauseToggle()
        self.startTime=None
        self.runTime=None
        self.runsCompleted=0
        self.xpGained=0
        self.moneyMade=0
        self.numCollected=0
        self.fastestTime=None

        self.updateText()

    def toggleLock(self,void=False):
        if not self.toggle:
            self.root.overrideredirect(True)
            self.root.attributes("-alpha", 0.7)
            self.root.wm_attributes("-topmost", 1)
            self.toggle=True
            
        else:
            self.root.overrideredirect(False)
            self.root.attributes("-alpha", 1)
            self.root.wm_attributes("-topmost", 0)
            
            self.toggle=False

    def tick(self):
        if not self.paused:
            if self.allowedNewRun:
                Input.checkBindings()
            self.updateText()
            
        self.root.after(20,self.tick)
        
class Collect:

    def __init__(self):
        self.root=Tk()
        self.root.title('Rs Paint')
        data=[]
        
        
        try:
            data=[]
            with open('Last Save.txt','r') as saveFile:
                for line in saveFile:
                    data.append(line.strip())
        except:
            data=['','','','','','']
            
            

        self.title=Label(self.root, text='Set Values', font=('Helvetica',20,"bold"))
        self.title.grid(row=0,column=0)

        self.searchFrame=Frame(self.root)
        self.searchFrame.grid(row=1,column=0)

        self.searchBox=Entry(self.searchFrame)
        self.searchBox.grid(row=0,column=0)
        self.searchBox.bind('<Return>',self.startThread1)
        
        self.searchButton=Button(self.searchFrame,text='Search', command=self.startThread1)
        self.searchButton.grid(row=0,column=1)

        self.optionText=Label(self.searchFrame,text='Select Item: ')
        self.optionText.grid(row=1,column=0)

        self.select1=StringVar()
        self.select1.set('None')
        self.selectList=OptionMenu(self.searchFrame,self.select1,'None')
        self.selectList.grid(row=1,column=1)
        

        self.itemPriceLabel=Label(self.searchFrame,text='Item Price: ')
        self.itemPriceLabel.grid(row=2,column=0)

        self.itemPrice=Entry(self.searchFrame)
        self.itemPrice.grid(row=2,column=1)
        self.itemPrice.insert(0, data[1])

        self.moneyLabel=Label(self.searchFrame,text='Money Spent Per Run:')
        self.moneyLabel.grid(row=3,column=0)
        
        self.moneySpent=Entry(self.searchFrame)
        self.moneySpent.grid(row=3,column=1)
        self.moneySpent.insert(0, data[2])

        self.itemsPerLabel=Label(self.searchFrame,text='Items Collected Per Run:')
        self.itemsPerLabel.grid(row=4, column=0)

        self.itemsPerRun=Entry(self.searchFrame)
        self.itemsPerRun.grid(row=4,column=1)
        self.itemsPerRun.insert(0, data[3])

        self.xpPerItemLabel=Label(self.searchFrame, text='Xp Per Item:')
        self.xpPerItemLabel.grid(row=5,column=0)

        self.xpPerItem=Entry(self.searchFrame)
        self.xpPerItem.grid(row=5,column=1)
        self.xpPerItem.insert(0, data[4])

        self.onNewRunText=Label(self.searchFrame, text='Extra commands (optional)')
        self.onNewRunText.grid(row=6,column=0)
        
        self.newRunCommand=Entry(self.searchFrame)
        self.newRunCommand.grid(row=6,column=1)
        self.newRunCommand.insert(0, data[5])

        self.getKeyButtonText=StringVar()
        self.getKeyButtonText.set('Click to set Banking button')

        self.bankKey=None
        
        self.getKeyButton=Button(self.root,textvar = self.getKeyButtonText,command=self.getKey)
        self.getKeyButton.grid(row=7,column=0)

        if data[0]:
            self.setKey(int(data[0]))
        
        self.startButton=Button(self.root,text='Start Paint',command=self.start)
        self.startButton.grid(row=8,column=0)


        self.allData=[self.itemPrice,self.moneySpent,self.itemsPerRun,self.xpPerItem]
        self.root.mainloop()

    def startThread1(self,void=None):
        self.resetOptions(['Loading'])
        threading.Thread(target=self.getItemDetails,args=()).start()

    def setKey(self,key):
        self.bankKey=key
        Input.ignoreAll(self.setKey)
        self.getKeyButtonText.set('Key Set')

    def getKey(self):
        self.getKeyButtonText.set('Getting Key')
        self.bankKey=None
        Input.bindAll(self.setKey)
        self.keyLoop()

    def keyLoop(self):
        if not self.bankKey:
            Input.checkBindings()
            self.root.after(10,self.keyLoop)
            
            

    def resetOptions(self,options):
        self.selectList.destroy()
        self.select1=StringVar()
        self.select1.set(options[0])
        self.selectList=OptionMenu(self.searchFrame,self.select1,*options,command=self.optionSelected)
        self.selectList.grid(row=1,column=1)

    def optionSelected(self,item):
        itemId=item.split(' : ')[-1]
        
        try:
            response=request.urlopen("http://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item=%s" %(itemId))
            itemDetails=eval(response.read())
            price=itemDetails['item']["current"]["price"]
            self.itemPrice.delete(0, END)
            self.itemPrice.insert(0,str(price))
            
            
        except:
            messagebox.showwarning("No Info","Item info not found on grand exchange")
        
        

    def getItemDetails(self):
        send='None'
        while send=='None':
            send = self.searchBox.get().replace(' ','+')
        
        response = str(requests.get('https://www.runelocus.com/tools/rs-item-id-list/?search=%s&order_by=itemlist_id' %(send), headers = {'user-agent': 'my-app/0.0.1'}).text)
        try:
            response = str(requests.get('https://www.runelocus.com/tools/rs-item-id-list/?search=%s&order_by=itemlist_id' %(send), headers = {'user-agent': 'my-app/0.0.1'}).text)
            table=response.split('<table class="table">')[-1].split('</thead>')[-1].split('</table>')[0]

            rows={}
            #print(table)
            for row in table.split('<tr>')[1:]+table.split('<tr class="alternate">')[1:]:
                
                row=row.split('</tr')[0]
                itemId=row.split('<td>')[1].split('</td>')[0]
                itemNameLink=row.split('</td>')[-2].split('td>')[-1]
                itemName=itemNameLink.split('">')[-1].split('</a>')[0]
                rows[int(itemId)]=itemName

            output=[]

            for key in list(collections.OrderedDict(sorted(rows.items()))):
                output.append(rows[key]+' : '+str(key))
                
            self.order=output
            
                
            if output:
                self.resetOptions(output)
                self.optionSelected(output[0])
            else:
                self.resetOptions(['None'])
        except:
            self.resetOptions(['NetworkError'])
            

    def start(self):
        runCommand=self.newRunCommand.get()
        
        if not self.newRunCommand.get():
            runCommand=None

        badData=False

        for data in self.allData:
            if not data.get():
                badData=True
                break
            try:
                float(data.get())
            except:
                badData=True
                break
            
        if badData:
            messagebox.showwarning("More Info","Please make sure all information is filled")
            return

        
        
        data=[
              self.bankKey,
              float(self.allData[0].get()),
              float(self.allData[1].get()),
              float(self.allData[2].get()),
              float(self.allData[3].get()),
              runCommand
        ]

        self.root.destroy()

        with open('Last Save.txt','w') as saveFile:
            for item in data:
                saveFile.write(str(item)+'\n')
            
        
        Paint(*data)
        
            
        
        
            
Collect()
