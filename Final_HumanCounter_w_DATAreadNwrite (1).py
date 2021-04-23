import RPi.GPIO as GPIO
import time
import os
import time 
from time import sleep
from datetime import datetime

TRIG =21
ECHO =20
GPIO.setmode(GPIO.BCM)
HumanCounter = 0
counter = 0
currentState1 = 0
previousState1 = 0
currentState2 = 0
previousState2 = 0
inside = 0
outside = 0

now = datetime.now()
file = open("/home/pi/BiDirectionalCounterData_v2.0.txt", "a")
file.write("Time, inside, outside, counter\n")
file.flush()

while True:
    #This counter use 1 ultra sonic sensor and check a target range
    #This program does not check for any errors
    # VERSION 1 : HumanCounter
    #print("distance measurement in progress")
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    #print("waiting for sensor to settle")
    time.sleep(0.2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    #distanceCM=round(distance,2)
    distance=distance/2.54
    print("     distance INCH:",distance,"in")
    #print("distance CM:",distanceCM,"cm")
    time.sleep(0.25)
############### STATE 1 DETECTION WITH IN 5in-10in
    ########### OBJECT DETECTED WALKING IN
    if distance > 10 and distance <= 39 :
            currentState1 = 1    
    else :
            currentState1 = 0;
    
    if currentState1 != previousState1:
             if currentState1 == 1:
                 print( "CurrentState2: In Detected", currentState1) 
                 counter = counter + 1
                 inside = inside +1
                 now = datetime.now()
                 file = open("/home/pi/BiDirectionalCounterData_v2.0.txt", "a")
                 file.write(str(now)+","+str(inside)+","+str(outside)+","+str(counter)+"\n")
                 file.flush()
    
############### STATE 2 DETECTION WITH IN 10in-15in
    ########### OBJECT DETECTED WALKING OUT
    if distance > 40 and distance <= 60:
             currentState2 = 1     
    else :
             currentState2 = 0
    if currentState2 != previousState2:
            if currentState2 == 1:
                print( "CurrentState2: Out Detected", currentState2)                
                counter = counter - 1
                outside = outside +1
                now = datetime.now()
                file = open("/home/pi/BiDirectionalCounterData_v2.0.txt", "a")
                file.write(str(now)+","+str(inside)+","+str(outside)+","+str(counter)+"\n")
                file.flush()
################
    print("   Inside:",inside,"   Outside:",outside)
    print("   Counter:",counter)
    print(" distance INCH:",distance,"in")
    
