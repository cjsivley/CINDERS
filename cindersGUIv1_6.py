#CINDERS GUI v.1.5
#11/08/2021
#Changes from 1.4
#fixed time logging bug
#working: selective pin activation
#todo: breakout mf into subframes


import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
#import RPi.GPIO as GPIO
import interceptGPIO as GPIO
import time #for timestamps and sleep

##################setup & global variables####################

#time setup
curTime = time.time()
print("CINDERS Start: " + time.strftime('%c', time.localtime(curTime)))

#pinout
#type 'pinout' into terminal to see diagram
sArray = [8,10,12,16] #array of solenoid control pins.

#user adjustable settings
relayDelayTime = 1 #delay to prevent DC Amp spike overloading.
gMW = 250 #gui min width
gMH = 50 #gui min height
GPIO.setwarnings(False)


#hardware initialization
#Relay Board is unintuitively HIGH = Off, LOW = On.
GPIO.setmode(GPIO.BOARD)
for each in sArray:
    GPIO.setup(each, GPIO.OUT, initial=GPIO.LOW)

#relay functions (where the work is done)
def relayON(pinArray):
    textLog = open("CINDERSlog.txt","a")
    msg = "Tank {} ON!!!"
    statusValue.set("Activating Tanks...")
    for tank, pin in enumerate(pinArray, start=1):
        #tank activation
        GPIO.output(pin, GPIO.HIGH)
        
        #status update stuff
        #stackabuse.com/formatting-strings-with-python
        #todo: create two frames in order to align data properly
        timeString = time.strftime('%m/%d/%Y(%a) %I:%M:%S %p %Z', time.localtime(time.time()))
        msgString = (msg.format(tank)) 
        logString = (timeString + msgString)
        logString = (f"{timeString:.<40}{msgString:.>30}")
        logs.insert(0, logString)
        textLog.write(str(logString) + "\n") #write to text log
        sc['state']='normal'
        logsHolder.set(logs) #update log values in gui
        sc['state']='disabled' #lock out listbox after editing
        
        #gui update
        lamp[tank-1].configure(image=lampOn)
        lamp[tank-1].image = lampOn
        
        mf.update_idletasks() #push to tk stringvar objects
        #hardware sleep to prevent amp spike
        time.sleep(relayDelayTime)
    statusValue.set("Tanks Engaged. CO2 Deploying.")
    textLog.close()
    
def relayOFF(pinArray):
    textLog = open("CINDERSlog.txt","a")
    msg = "Tank {} OFF!!!"
    for tank, pin in enumerate(pinArray, start=1):
        GPIO.output(pin, GPIO.LOW)
        
        #status update stuff
        timeString = time.strftime('%m/%d/%Y(%a) %I:%M:%S %p %Z', time.localtime(time.time()))
        msgString = (msg.format(tank)) 
        logString = (timeString + msgString)
        logString = (f"{timeString:.<40}{msgString:.>30}")
        logs.insert(0, logString)
        textLog.write(str(logString) + "\n") #write to text log
        sc['state']='normal'
        logsHolder.set(logs) #update log values in gui
        sc['state']='disabled' #lock out listbox after editing
        
        #lamp update
        #gui update
        lamp[tank-1].configure(image=lampOff)
        lamp[tank-1].image = lampOff
        
        mf.update_idletasks() #push to tk stringvar objects
        #no need to sleep, power off doesn't cause amp spike
    statusValue.set("Tanks closed, CO2 Halted")
    textLog.close()

######################################GUI CODE#########################################
window = tk.Tk()
window.title("CINDERS")

#image init
lampOn = Image.open("red-dome-light-on.jpg")
lampOff = Image.open("red-dome-light-off.jpg")
#image cleanup
lampOn = lampOn.resize((100,100), Image.ANTIALIAS)
lampOff = lampOff.resize((100,100), Image.ANTIALIAS)
lampOn = ImageTk.PhotoImage(lampOn)
lampOff = ImageTk.PhotoImage(lampOff)

mf = ttk.Frame(window) #mf = main frame
mf.grid(column=0, row=0, sticky=("nsew"))
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
#grid config of mainframe:
#col/row = 0,0 because it fills the entire window.
#sticky all sides, weight even, same reason

#configure mf grid
for i in range (3):
    mf.rowconfigure(i, weight=1, minsize=gMH)
for i in range (2):
    mf.columnconfigure(i, weight=1, minsize=gMW)

#mf grid children
btnEngage = tk.Button(
    text="Engage",
    font=("Arial",24),
    master=mf,
    borderwidth=2,
    bg="#3f9c17",
    activebackground="#52c91e",
    command = lambda: relayON(sArray) #lambda delays command until click
    )
btnEngage.grid(row=0,column=0,padx=5,pady=5,sticky="nsew")

btnDisengage = tk.Button(
    text="Disengage",
    font=("Arial",24),
    master=mf,
    borderwidth=2,
    bg="#ba3622",
    activebackground="#d93f27",
    command = lambda: relayOFF(sArray)
    )
btnDisengage.grid(row=0,column=1,padx=5,pady=5,sticky="nsew")
#active pin/tanks display
td = ttk.Frame(mf) #td = tank display
td.grid(row=1, column=0, columnspan=2, sticky="nsew")
td.rowconfigure(1, weight=1)
for i in range (5):
    td.columnconfigure(i, weight=1)
#creation of lamp labels

lamp1 = ttk.Label(td, text='Tank 1', image=lampOff, compound="top")
lamp2 = ttk.Label(td, text='Tank 2', image=lampOff, compound="top")
lamp3 = ttk.Label(td, text='Tank 3', image=lampOff, compound="top")
lamp4 = ttk.Label(td, text='Tank 4', image=lampOff, compound="top")
lamp1.grid(row=1, column=1, sticky= "ew")
lamp2.grid(row=1, column=2, sticky= "ew")
lamp3.grid(row=1, column=3, sticky= "ew")
lamp4.grid(row=1, column=4, sticky= "ew")

lamp = [lamp1, lamp2, lamp3, lamp4]

#status console
logs = []
logsHolder = tk.StringVar(mf, value=logs)

sc = tk.Listbox( #status console
    master=mf,
    height=5,
    listvariable=logsHolder)
sc['state']='disabled'
sc.grid(row=3, column=0, columnspan=2, sticky="we")
scScroll = tk.Scrollbar(
    master=mf,
    orient="vertical",
    command=sc.yview)
scScroll.grid(row=3, column=2, sticky="ns")
sc['yscrollcommand']=scScroll.set

#display text variables
statusLabel = tk.Label(mf, text="Status: ")
statusLabel.grid(row=2, column=0, padx=5, pady=5,sticky="sw")

statusValue=tk.StringVar(mf, "Waiting")
statusDisplay = tk.Label(mf,textvariable=statusValue)
statusDisplay.grid(row=2, column=1, padx=5, pady=5, sticky="se")

#main loop
window.mainloop()