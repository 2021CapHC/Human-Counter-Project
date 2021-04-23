"""
 _    _                                _____                  _               _____ _______ _    _ 
| |  | |                              / ____|                | |             / ____|__   __| |  | |
| |__| |_   _ _ __ ___   __ _ _ __   | |     ___  _   _ _ __ | |_ ___ _ __  | |       | |  | |  | |
|  __  | | | | '_ ` _ \ / _` | '_ \  | |    / _ \| | | | '_ \| __/ _ \ '__| | |       | |  | |  | |
| |  | | |_| | | | | | | (_| | | | | | |___| (_) | |_| | | | | ||  __/ |    | |____   | |  | |__| |
|_|  |_|\__,_|_| |_| |_|\__,_|_| |_|  \_____\___/ \__,_|_| |_|\__\___|_|     \_____|  |_|   \____/ 
                                                                                                    
╔═╗┬┌┐┌┌─┐┬  ┌─┐  ╔═╗┌┐┌┌┬┐┬─┐┬ ┬
╚═╗│││││ ┬│  ├┤   ║╣ │││ │ ├┬┘└┬┘
╚═╝┴┘└┘└─┘┴─┘└─┘  ╚═╝┘└┘ ┴ ┴└─ ┴

"""                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

import RPi.GPIO as GPIO
import time
from time import sleep
from datetime import datetime
import os

#HumanCounter system for a Single Entry Door
#Uses 2 UltraSonic Sensors to Detect People Walking In and Out of Entry way
#Error Detection for Objects Not Walking In or Out Fully as well as Blocked Objects

#Ultra Sonic Sensor 1 ( Inner )
echoPin1 =20
trigPin1 =21
#Ultra Sonic Sensor 2 ( Outter )
echoPin2 =23
trigPin2 =24

#When Current State Changes Detection Occurs
#When Current State Stays 0 No Detection
#Previoustate is always 0
currentState1 = 0;
previousState1 = 0;
currentState2 = 0;
previousState2 = 0;

#Data Related Counters
HumanCounter = 0
counter = 0
inside = 0
outside = 0

#GPIO Setup Input/Outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigPin1,GPIO.OUT)
GPIO.setup(echoPin1,GPIO.IN)
GPIO.setup(trigPin2,GPIO.OUT)
GPIO.setup(echoPin2,GPIO.IN)

#
now = time.strftime("%b %d %Y %r")
file = open("/home/pi/Desktop/FinalCodesHumanCounter/SingleEntryData.txt", "a")
file.write("Time, inside, outside, counter\n")
file.flush()

while True:
    #Double Check Sensors for Error (Runs Loop to check sensor multiple times)
    DoubleCheck = 0
#############################################################
#######Checks UltraSonicSesnor Distance for Sensor 1 (Inner)
    GPIO.output(trigPin1,False)
    #time.sleep(0.2)
    time.sleep(0.1)
    GPIO.output(trigPin1,True)
    time.sleep(0.00001)
    GPIO.output(trigPin1,False)
    while GPIO.input(echoPin1)==0:
        pulse_start1=time.time()
    while GPIO.input(echoPin1)==1:
        pulse_end1=time.time()
    pulse_duration1=pulse_end1-pulse_start1
    distance1=pulse_duration1*17150
    distance1=distance1/2.54
   #print("     distance1 INCH:",distance1,"in")
#^^^^^^^Uncomment if you would like to see Distance Readings for USsensor1
    
    time.sleep(0.001) #Short delay so no signals between sensors can cause errors
    
#############################################################
#######Checks UltraSonicSesnor Distance for Sensor 2 (Outter)
    GPIO.output(trigPin2,False)
    #time.sleep(0.2)
    time.sleep(0.1)
    GPIO.output(trigPin2,True)
    time.sleep(0.00001)
    GPIO.output(trigPin2,False)
    while GPIO.input(echoPin2)==0:
        pulse_start2=time.time()
    while GPIO.input(echoPin2)==1:
        pulse_end2=time.time()
    pulse_duration2=pulse_end2-pulse_start2
    distance2=pulse_duration2*17150
    distance2=distance2/2.54
    #print("     distance2 INCH:",distance2,"in")
#^^^^^^^Uncomment if you would like to see Distance Readings for USsensor2
    
######################################################
###################################################### 
###### OBJECT ENTERING IN THE SYSTEM
    if distance1 > 1 and distance1 <= 10:
             currentState1 = 1; #DETECTED OBJECT INFRONT OF SENSOR 1
    else: 
             currentState1 = 0; #NO DETECTION INFRONT OF SENSOR 1
             
    if currentState1 != previousState1: #IF DETECTED
            while currentState1 == 1:
#IF SENSOR 1 DETECTS MAKESURE OBJECT WALKS PAST SENSOR 2 AS WELL
                GPIO.output(trigPin2,False)
                time.sleep(0.1)
                GPIO.output(trigPin2,True)
                time.sleep(0.00001)
                GPIO.output(trigPin2,False)
                while GPIO.input(echoPin2)==0:
                    pulse_start2=time.time()
                while GPIO.input(echoPin2)==1:
                    pulse_end2=time.time()
                pulse_duration2=pulse_end2-pulse_start2
                distance2=pulse_duration2*17150
                distance2=distance2/2.54
                   #print("     distance2 INCH:",distance2,"in")
            #^^^^^^^Uncomment if you would like to see Distance Readings for USsensor2
                if distance2 > 1 and distance2 <= 10: #IF DETECTION @ SENSOR 2 THAN OBJECT WALKED IN FULLY
                     currentState2 = 1;
                     print( "CurrentState1: In Detected", currentState1) 
                     counter = counter + 1 #ADD TO CURRENT COUNT
                     inside = inside +1 #ADD TO TALLY OF NUMBER OF IN'S
#### DATA  READ AND WRITE ######### DATA  READ AND WRITE ######### DATA  READ AND WRITE #####
                     now = datetime.now()
                     file = open("/home/pi/Desktop/FinalCodesHumanCounter/SingleEntryData.txt", "a")
                     file.write(str(now)+","+str(inside)+","+str(outside)+","+str(counter)+"\n")
                     file.flush()
##PRINT########PRINT########PRINT########PRINT########PRINT########PRINT########PRINT########PRINT######
                     print("   Inside:",inside,"   Outside:",outside)
                     print("   Counter:",counter)
                     print(" distance1 INCH:",distance1,"in")
                     time.sleep(0.4)
                     currentState1 = 0 #EXITS OUT OF WHILE LOOP ABOVE AND STARTS PROGRAM FROM TOP
                else: #IF NO DETECTION AT SENSOR 2 OBJECT DID NOT WALK IN FULLY
                     currentState2 = 0;
                     DoubleCheck = DoubleCheck + 1 #SYSTEM WILL DOUBLE CHECK 6 TIMES FOR OBJECT TO PASS
                     if DoubleCheck == 5: #IF OBJECT DOES NOT WALK IN AFTER 6 CHECKS RETURN TO BEGINING OF PROGRAM
                         print(" OBJECT DID NOT WALK IN FULLY:", currentState1)
                         currentState1 = 0 #EXITS OUT OF WHILE LOOP ABOVE AND STARTS PROGRAM FROM TOP
                         time.sleep(0.4) #DELAY NEEDED TO NO CAUSE ERRORS


######################################################
###################################################### 
###### OBJECT EXITING OUT THE SYSTEM
    if distance2 > 1 and distance2 <= 10:
         currentState2 = 1; #DETECTED OBJECT INFRONT OF SENSOR 2
    else:
         currentState2 = 0; #DETECTED OBJECT INFRONT OF SENSOR 2

    if currentState2 != previousState2: #IF DETECTED
            while currentState2 == 1:
#IF SENSOR 2 DETECTS MAKESURE OBJECT WALKS PAST SENSOR 1 AS WELL
                GPIO.output(trigPin1,False)
                #time.sleep(0.2)
                time.sleep(0.1)
                GPIO.output(trigPin1,True)
                time.sleep(0.00001)
                GPIO.output(trigPin1,False)
                while GPIO.input(echoPin1)==0:
                    pulse_start1=time.time()
                while GPIO.input(echoPin1)==1:
                    pulse_end1=time.time()
                pulse_duration1=pulse_end1-pulse_start1
                distance1=pulse_duration1*17150
                distance1=distance1/2.54
            #    print("     distance1 INCH:",distance1,"in")
    #^^^^^^^Uncomment if you would like to see Distance Readings for USsensor2
                if distance1 > 1 and distance1 <= 10: #IF DETECTION @ SENSOR 1 THAN OBJECT WALKED OUT FULLY
                     currentState1 = 1;
                     print( "CurrentState2: Out Detected", currentState2)                
                     counter = counter - 1 # REMOVES FROM CURRENT COUNT
                     outside = outside +1  # ADDS TO TALLY OF NUMBER OF OUTS
#### DATA  READ AND WRITE ######### DATA  READ AND WRITE ######### DATA  READ AND WRITE #####
                     now = datetime.now()
                     file = open("/home/pi/Desktop/FinalCodesHumanCounter/SingleEntryData.txt", "a")
                     file.write(str(now)+","+str(inside)+","+str(outside)+","+str(counter)+"\n")
                     file.flush()
##PRINT########PRINT########PRINT########PRINT########PRINT########PRINT########PRINT########PRINT######
                     print("   Inside:",inside,"   Outside:",outside)
                     print("   Counter:",counter)
                     print(" distance2 INCH:",distance2,"in")
                     time.sleep(0.4)
                     currentState2 = 0 #EXITS OUT OF WHILE LOOP ABOVE AND STARTS PROGRAM FROM TOP
                else: #IF NO DETECTION AT SENSOR 1 OBJECT DID NOT WALK OUT FULLY
                     currentState1 = 0;
                     DoubleCheck = DoubleCheck + 1 #SYSTEM WILL DOUBLE CHECK 6 TIMES FOR OBJECT TO PASS
                     if DoubleCheck == 5: #IF OBJECT DOES NOT WALK OUT AFTER 6 CHECKS RETURN TO BEGINING OF PROGRAM
                         print(" OBJECT DID NOT WALK OUT FULLY:", currentState2)
                         currentState2 = 0 #EXITS OUT OF WHILE LOOP ABOVE AND STARTS PROGRAM FROM TOP
                         time.sleep(0.4)#DELAY NEEDED TO NO CAUSE ERRORS
