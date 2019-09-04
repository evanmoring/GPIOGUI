import tkinter
import time
import RPi.GPIO as GPIO
import threading

currentRefreshRate = 100

GPIO.setmode(GPIO.BOARD)
pinList=[False]
boardType = [False,0,1,3,1,3,2,3,3,2,3,3,3,3,2,3,3,0,3,3,2,3,3,3,3,2,3,4,4,3,2,3,3,3,2,3,3,3,3,2,3]
pinTypeKey = ['3V3','5v','GND','GPIO','Empty']
bcmDict = {3:2,5:3,7:4,8:14,10:15,11:17,12:18,13:27,15:22,16:23,18:24,19:10,21:9,22:25,23:11,24:8,26:7,29:5,31:6,32:12,33:13,35:19,36:16,37:26,38:20,40:21}
portUse = {0:"GPIO.OUT", 1:"GPIO.IN",40:"GPIO.SERIAL",41:"GPIO.SPI",42:"GPIO.I2C",43:"GPIO.HARD_PWM", -1:"GPIO.UNKNOWN"}
voltageDict = {0:"Low", 1:"High",2:"Pin not set"}
gpioList = []

gNum = 0
for i in boardType:
    if i ==3:
        gpioList.append('Pin ' + str(gNum))
    gNum+=1
    
useList = []
for i in portUse:
    useList.append(portUse[i])

def doForAllPins(function):
    for r in range(1,len(boardType)):
        function(r)

def checkPin(pinNumber):
    cPin = pinList[pinNumber]
    cPin.type.value=pinTypeKey[boardType[pinNumber]]
    if cPin.type.value=='GPIO':
        cPin.usage.value = portUse[GPIO.gpio_function(pinNumber)]
        cPin.voltage.value=voltageDict[voltage(pinNumber)]
        cPin.bcm.value = bcmDict[pinNumber]

def voltage(pin):
    try:
        return(GPIO.input(pin))
    except:
        return(2)
    
def checkAllPins():
    doForAllPins(checkPin)

def cleanPin(i):
    if boardType[i]==3:
        GPIO.setup(i,GPIO.OUT)
        GPIO.output(i,0)
        GPIO.setup(i,GPIO.IN)

def cleanAll():
        doForAllPins(cleanPin)

cleanAll()

class pin:
    def __init__(self,pinNum):
        self.number = pinAttribute()
        self.number.value=pinNum
        self.type=pinAttribute()
        self.bcm=pinAttribute()
        self.usage=pinAttribute()
        self.voltage=pinAttribute()

class pinAttribute:
    def __init__(self):
        self.value = False
        self.address = False

for i in range(1,len(boardType)):
    pinList.append(pin(i))
    cPin = pinList[i]
    cPin.type.value=pinTypeKey[boardType[i]]
    if cPin.type.value=='GPIO':
        cPin.usage.value = portUse[GPIO.gpio_function(i)]
        cPin.voltage.value=voltageDict[voltage(i)]
        cPin.bcm.value = bcmDict[i]
        
def gui():
    root = tkinter.Tk(  )
    root.title('GPIO GUI')
    menuGrid = tkinter.Frame(root)
    menuGrid.pack( side = 'left',fill='y')
    pinGrid = tkinter.Frame(root, borderwidth = 1, relief ="solid" )
    pinGrid.pack( side='right')
    pinUpdate = tkinter.Frame(menuGrid)
    pinUpdate.pack()
    pinReset = tkinter.Frame(menuGrid)
    pinReset.pack(fill='x')
    refreshRate = tkinter.Frame(menuGrid)
    refreshRate.pack(side = "bottom")

    pinRowOffset = 0
    pinColumnOffset = 10
    
    def header(text,column):
        tkinter.Label(pinGrid,text=text).grid(row=pinRowOffset,column=column+pinColumnOffset)
        tkinter.Label(pinGrid,text=text).grid(row=pinRowOffset,column=column+pinColumnOffset+5)

    header('#',1)
    header('Type',2)
    header('BCM',3)
    header('Usage',4)
    header('Voltage',5)

    rowNumber = ''
    columnNumber = ''
    colorDict = {'High':'Red','Low':'Blue','GPIO.IN':'Green','GPIO.OUT':'Purple','GPIO':'Purple'}
    
    def populateTable(pinNum):
        cPin = pinList[pinNum]
        global rowNumber, columnNumber
        pinType = pinTypeKey[boardType[pinNum]]
        if pinNum%2 == 0:
            rowNumber = int((pinNum+1)/2)
            columnNumber = 6
        if pinNum%2== 1:
            rowNumber = int((pinNum+2)/2)
            columnNumber = 1
        gridCell(cPin.number,0)
        gridCell(cPin.type,1)
        if cPin.type.value == 'GPIO':
            
            gridCell(cPin.bcm,2)
            if cPin.usage.value== 'GPIO.IN' and cPin.voltage==2:
                gridCell('PNS',3,pinNum)
                gridCell(cPin.voltage, 4)
            else:
                gridCell(cPin.usage,3,colorDict[cPin.usage.value])
                gridCell(cPin.voltage, 4,colorDict[cPin.voltage.value])
        
    def gridCell (attribute, columnOffset,*colorChoice):
        global rowNumber, columnNumber
        color = 'Black'
        if colorChoice:
            color = colorChoice
        if attribute.address==False:
            attribute.address=tkinter.Label(pinGrid,text='%s'%(attribute.value),fg=color,borderwidth=1)
            attribute.address.grid(row=rowNumber+pinRowOffset,column =columnNumber+columnOffset+pinColumnOffset)
        else:
            if attribute.value != attribute.address["text"]:
                attribute.address.config(text='%s'%(attribute.value),fg=color)

    def checkAndPopulate():
        checkAllPins()
        populateAll()
        root.after(currentRefreshRate,checkAndPopulate)

    def populateAll():
        doForAllPins(populateTable)

    def getPinChoice():
        oldString = (pinChoice.get())
        newString = ''
        for i in oldString:
            if (i).isdigit() == True:
                newString+=i
        return int(newString)
    
    def updatePin():
        cPin = getPinChoice()
        cUsage = usageChoice.get()
        cPull = pullChoice.get()
        if cUsage == 'GPIO.IN':
            GPIO.setup(cPin,GPIO.IN)
        if cUsage == 'GPIO.OUT':
            if voltageChoice.get() == 'HIGH':
                GPIO.setup(cPin,GPIO.OUT,initial=1)
            else:
                GPIO.setup(cPin,GPIO.OUT,initial = 0)
        else:
            if cPull=='None':
                GPIO.setup(cPin,GPIO.IN,pull_up_down=GPIO.PUD_OFF)
            if cPull=='Pull Down':
                GPIO.setup(cPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
            if cPull=='Pull Up':
                GPIO.setup(cPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)


    menuRow = 1
    menuColumn = 1

    pinChoice = tkinter.StringVar(pinUpdate)
    pinChoice.set(gpioList[0])
    pinMenu= tkinter.OptionMenu(pinUpdate, pinChoice,*gpioList)
    pinMenu.grid(row=menuRow,column =menuColumn)
    
    usageChoice = tkinter.StringVar(pinUpdate)
    usageChoice.set('GPIO.IN')
    usageMenu= tkinter.OptionMenu(pinUpdate, usageChoice,*['GPIO.IN','GPIO.OUT'])
    usageMenu.grid(row=menuRow,column =menuColumn+1)

    voltageChoice = tkinter.StringVar(pinUpdate)
    voltageChoice.set('LOW')
    voltageMenu= tkinter.OptionMenu(pinUpdate, voltageChoice,*['LOW','HIGH'])
    voltageMenu.grid(row=menuRow,column =menuColumn+2)

    pullChoice = tkinter.StringVar(pinUpdate)
    pullChoice.set('Pull Up')
    pullMenu= tkinter.OptionMenu(pinUpdate, pullChoice,*['Pull Down','Pull Up', 'None'])
    pullMenu.grid(row=menuRow,column =menuColumn+3)

    updateButton= tkinter.Button(pinUpdate,text = "Update",command = updatePin)
    updateButton.grid(row=menuRow,column=menuColumn+5)  

    resetButton= tkinter.Button(pinReset,text = "Reset all pins",command = cleanAll)
    resetButton.pack(side="right")

##    refreshLabel = tkinter.Label(refreshRate,text='Current Refresh Rate: ' + str(currentRefreshRate)+ 'ms').grid(row=1,column = 2, sticky = "E")
##
##    refreshChoice = tkinter.StringVar
##    refreshEntry = tkinter.Entry(refreshRate)
##    refreshEntry.grid(row=2,column = 2, sticky = 'SE')

##    refreshLabel = tkinter.Label(refreshRate,text='Refresh Rate').grid(row=2,column=1, sticky = "SE")

##    pinEntry = tkinter.Entry()
##    pinEntry.grid(row=menuRow,column= menuColumn)
    
    checkAndPopulate()
        
    root.mainloop(  )
t1= threading.Thread(target=gui, name='t1')
t1.start()

