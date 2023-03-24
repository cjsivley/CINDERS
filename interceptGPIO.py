# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 12:23:38 2022

@author: User
"""

#GPIO Interceptor
#designed to intercept RPI.GPIO commands:
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(each, GPIO.OUT, initial=GPIO.LOW)
# GPIO.output(pin, GPIO.HIGH)
# GPIO.output(pin, GPIO.LOW)

def setwarnings(arg):
    print("setwarnings has turned warnings: " + str(arg))
    
def setmode(arg):
    print("setmode has set mode to: " + str(arg))
    
def setup(*args, **kw):
    print("Setup: ")
    for each in args:
        print(str(each))
    for each in kw:
        print(str(each))
    
def output(pin, level):
    print("Pin " + str(pin) + " is " + str(level))
    
BOARD = "BOARD"
HIGH = "HIGH"
LOW = "LOW"
IN = "IN"
OUT = "OUT"