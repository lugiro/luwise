#!/usr/bin/env python
"""
================================================
ABElectronics Servo Pi pwm controller | PWM servo controller demo

run with: python demo_servomove.py
================================================

This demo shows how to set the limits of movement on a servo
and then move between those positions
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os
import tty, termios, sys

try:
    from ServoPi import Servo
except ImportError:
    print("Failed to import ServoPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from ServoPi import Servo
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")



def init():
    """
    Main program function
    """
    # create an instance of the servo class on I2C address 0x40
    global servo
    servo = Servo(0x40)

    # set the servo minimum and maximum limits in milliseconds
    # the limits for a servo are typically between 1ms and 2ms.

    servo.set_low_limit(0.5)
    servo.set_high_limit(2.5)

    # Enable the outputs
    servo.output_enable()


def startInfo(version,versiondate):
    print ("**********************************")
    print ("*              LOS               *")
    print ("*    Luwise Operating System     *")
    print ("*          Version",version,"         *")
    print ("*      Press h to get HELP       *")
    print ("**********************************")


#Show servo numbers
def robotDraw(file):
    f = open(file, 'r')
    Lines = f.readlines()
    numberOfLines = len(open(file).readlines(  ))
    f.close()
    for lineNum in range(0, numberOfLines, 1):
       line = Lines[lineNum].strip('\n')
       print (line)


#Return a single character from standard input
def getchar():
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch


#Move one servo to position x
def moveServo(servonum,position):
    if servonum >= 1 and servonum <= 16:
       servo.move(servonum,position)
    if servonum >= 17 and servonum <= 32:
       servoB2.move(servonum,position)


#Get servo position
def getServoPosition(servonum):
    if servonum >= 1 and servonum <= 16:
       servopos = servo.get_position(servonum)
    if servonum >= 17 and servonum <= 32:
       servopos = servoB2.get_position(servonum)
    return servopos


#move servo in pluss/minus direction
def movPlussMinus(servoNum, stepMin, stepMax, stepSize):
    print ("Move servo",servoNum," (use +/0)")
    ch = getchar()
    while ch.strip() == '+' or ch.strip() == '0':
       if ch.strip() == '+':
          while ch.strip() == '+':
             servoPos = getServoPosition(servoNum)
             if servoPos < stepMax-stepSize+1:
                moveServo(servoNum, servoPos+stepSize)
             step = getServoPosition(servoNum)
             print ("Servo",servoNum,"step:",step)
             ch = getchar()
       if ch.strip() == '0':
          while ch.strip() == '0':
             servoPos = getServoPosition(servoNum)
             if servoPos > (stepMin+stepSize-1):
                moveServo(servoNum, servoPos-stepSize)
             step = getServoPosition(servoNum)
             print ("Servo",servoNum,"step:",step)
             ch = getchar()
    servoPos = getServoPosition(servoNum)
    return servoPos


#Adjust step size
def stepS(stepSize):
    stepS = stepSize
    print ("Adjust step size - use +/0: ",stepSize)
    ch = getchar()
    while ch.strip() == '+' or ch.strip() == '0':
       if ch.strip() == '+':
          while ch.strip() == '+':
             stepS = stepS + 1
             print ("Set step size : ",stepS)
             ch = getchar()
       if ch.strip() == '0':
          while ch.strip() == '0':
             stepS = stepS - 1
             print ("Set step Size :",stepS)
             ch = getchar()
    return stepS


#Save one movement cykle
def saveRobotData(file,NUMBERofSERVOS,servoPOS,delay):
    print ("Saved cycle data")
    moveData =  ""
    for servoNum in range(1, NUMBERofSERVOS+1, 1):
       formatcode ="{0:4}"
       data = (formatcode.format(servoPOS[servoNum]))
       moveData = moveData + data
    print (moveData)
    print (delay)
    moveData = moveData + "\n"
    delayData = (str(delay)+"\n")
    f= open(file,"a")
    f.write(moveData)
    f.write(delayData)
    f.close()


#Create a new project file
def newProject(file):
    f= open(file,"w")
    f.close()


#move all defined servoes
def moveAllServos(NUMBERofSERVOS,angle,speed):
    #Arranged servo numbers acording do RPi servo boards
    #IKKE I BRUK
    #servoN = [0,1,2,3,4,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    servoPOSn = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    STEP = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    stepCOUNTER = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    stepSERVO = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    COUNT = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    stepLIST = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for servoNum in range(1, NUMBERofSERVOS+1, 1):
#       servoPOSn[servoNum] = getServoPosition(servoN[servoNum])  Se over, eksempel paa bruk av servoN
       servoPOSn[servoNum] = getServoPosition(servoNum)
       STEP[servoNum] = angle[servoNum] - servoPOSn[servoNum]
       stepCOUNTER[servoNum] = STEP[servoNum]
       stepSERVO[servoNum] = 0
       if STEP[servoNum] >= 0:
          COUNT[servoNum] = 1
       else:
          COUNT[servoNum] = -1

    #Find max step counter
    for servoNum in range(1, NUMBERofSERVOS+1, 1):
       stepAbsValue = abs(STEP[servoNum])
       stepLIST.insert(servoNum, stepAbsValue)
    loopcounter = max(stepLIST)
    #print ("loop",loopcounter,stepLIST)

    #move six servos with highest stepp
    for pos in range(0, loopcounter, 1):
        time.sleep(speed)
        for servoNum in range(1, NUMBERofSERVOS+1, 1):
           if stepCOUNTER[servoNum] != 0:
              stepCOUNTER[servoNum] = stepCOUNTER[servoNum] - COUNT[servoNum]
              stepSERVO[servoNum] = stepSERVO[servoNum] + COUNT[servoNum]
              moveServo(servoNum, servoPOSn[servoNum]+stepSERVO[servoNum])
        #print (stepCOUNTER[1],stepCOUNTER[2],stepCOUNTER[3],stepCOUNTER[4],stepCOUNTER[5],stepCOUNTER[6])
        print (stepCOUNTER)


#Read movement data from file
def readMoveData(file):
   f = open(file, 'r') 
   Lines = f.readlines() 
   numberOfLines = len(open(file).readlines(  ))
   f.close()
   return numberOfLines, Lines


#Append movement data to excisting file
def appendMoveData(toFile,fromFile):
    numberOfLines, Lines = readMoveData(fromFile)
    f= open(toFile,"a")
    for lineNum in range(0, numberOfLines, 1):
       line = Lines[lineNum]
       f.write(str(line))
    f.close()

#Move the robot servos according to stored movement data
def moveRobot(file,NUMBERofSERVOS, speed, zeroANGLE):
    angle = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    numberOfLines, Lines = readMoveData(file)
    print ("Go to zero position first ? (y/n):")
    inputTerm = raw_input()
    if inputTerm == "y": 
       goToZero(NUMBERofSERVOS,zeroANGLE)
    for lineNum in range(0, numberOfLines, 2):
       line1 = Lines[lineNum]
       line2 = Lines[lineNum+1]
       cPos1 = 1
       cPos2 = 4
       for servoNum in range(1, NUMBERofSERVOS+1, 1):
          #print (angle[servoNum],cPos1,cPos2)
          angle[servoNum] = int(line1[cPos1:cPos2])
          cPos1 = cPos1 + 4
          cPos2 = cPos2 + 4
       moveAllServos(NUMBERofSERVOS,angle,speed)
       delay = float(line2)
       print (" ")
       print (angle)
       print (delay)
       time.sleep(delay)


def moveCycleByCyckle(dir,fileName,file,NUMBERofSERVOS, speed, zeroANGLE):
    angle = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    numberOfLines, Lines = readMoveData(file)
    print ("Go to zero position first ? (y/n):")
    inputTerm = raw_input()
    if inputTerm == "y": 
       goToZero(NUMBERofSERVOS,zeroANGLE)
       #pass
    #else:

    for lineNum in range(0, numberOfLines, 2):
       print (" ")
       print ("Cyckle by cycle (save: stop and save, q: quit) next cycle  press CR ")
       inputTerm = raw_input()
       if inputTerm == "q": #quit
          break
       if inputTerm == "save": #stop and save previos cycles, OBS overwrite excisting file
          backupFile(file)
#          fileC1 = dir + fileName+"-c1.mov"
#          fileC2 = dir + fileName+"-c2.mov"
          fileC1 = dir + "c1.mov"
          fileC2 = dir + "c2.mov"
          f= open(fileC1,"w")
          for lNum in range(0, lineNum-2, 1):
             f.write(Lines[lNum])
          f.close()
          f= open(fileC2,"w")
          for lNum in range(lineNum, numberOfLines, 1):
             f.write(Lines[lNum])
          f.close()
          break
       else:
          line1 = Lines[lineNum]
          line2 = Lines[lineNum+1]
          cPos1 = 1
          cPos2 = 4
          for servoNum in range(1, NUMBERofSERVOS+1, 1):
             #print (angle[servoNum],cPos1,cPos2)
             angle[servoNum] = int(line1[cPos1:cPos2])
             cPos1 = cPos1 + 4
             cPos2 = cPos2 + 4
          moveAllServos(NUMBERofSERVOS,angle,speed) 
          delay = float(line2)
          print (" ")
          print (angle)
          print (delay)
          time.sleep(delay)

#Read movement data from file and list data
def listMoveData(file):
    numberOfLines, Lines = readMoveData(file)
    for lineNum in range(0, numberOfLines, 1):
       line = Lines[lineNum].strip('\n')
       print (line)


#Raw/fast setting of zero position without, remember to use goToZero before quit
def setZeroPos(NUMBERofSERVOS,zeroAngle):
    #sette start posisjon
    for servoNum in range(1, NUMBERofSERVOS+1, 1):
       moveServo(servoNum,zeroAngle[servoNum])


#Go smooth to zero position
def goToZero(NUMBERofSERVOS,zeroAngle):
   speed = 0.01
   for servoNum in range(1, NUMBERofSERVOS+1, 1):
      moveAllServos(NUMBERofSERVOS,zeroAngle,speed)


#Show all task files
def showTaskFiles():
   cmd = "ls *.mov"
   os.system(cmd)

#Backup existing file before new file
def backupFile(file):
   cmd = "cp "+file+" "+file+"BAC"
   os.system(cmd)

#Test funktion
def test(NUMBERofSERVOS):
   for servoNum in range(1, NUMBERofSERVOS+1, 1):
      print ("test", NUMBERofSERVOS, servoNum)


#Controll modul for menu and execution
def controlModule():

   #startup value
   version = "2.02"
   versiondate = "27.06.2020"
   NUMBERofSERVOS = 6
   stepSize = 10               #step size for programming servos
   speed = 0.01                #speed for running task
   delay = 0.0                 #delay between task cycles

   fileName = "task0"          #default task file name
   ext = ".mov"                #file extention for task file
   dir = "/home/pi/RobotMan/"
   file = dir + fileName + ext #Task file
   drawFile = "robotDraw.txt"   #Draw file with servo numbers
   dFile = dir + drawFile

   #Actuall servo position
   servoPOS = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
   #Minimum allowed step/angle for servos
   stepMIN = [0,0,0,0,25,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
   #Maximum allowed step/angle for servos
   stepMAX = [0,225,200,250,220,215,87,99,99,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
   #Zero position (rest positon) for servos
   zeroANGLE = [0,80,30,127,125,125,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

   #Arranged servo numbers acording do RPi servo boards
   #servoNX = [0,1,2,3,4,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
   # IKKE I BRUK - SE sub


   #Raw/fast setting of zero position without, remember to use goToZero before quit
   setZeroPos(NUMBERofSERVOS,zeroANGLE)

   #Get actual servo position
   for servoNum in range(1, NUMBERofSERVOS+1, 1):
      servoPOS[servoNum] = getServoPosition(servoNum)
   print (servoPOS)

   startInfo(version,versiondate)

   while 1:
       print (" ")
       print ("New COMMAND:")
       inputTerm = raw_input()
       if inputTerm == "q": #quit
          print('bye!')
          break
       else:
          command = inputTerm

          if command == 'c':
             stepSize = stepS(stepSize)

          if command == 'p':
             print ("Programming servos ")
             for servoNum in range(1, NUMBERofSERVOS+1, 1): #get servo posotion
                servoPOS[servoNum] = getServoPosition(servoNum)
             while inputTerm <> "q":
                print (" ")
                print ("Choose servo number:")
                while True:
                   try:
                      inputTerm = raw_input()
                      if inputTerm == "q": #quit
                         pass
                      else:
                         servoNum = int(inputTerm)
                         if servoNum >= 1 and servoNum <= NUMBERofSERVOS:
                            print (command, servoNum)
                            servoPOS[servoNum] = movPlussMinus(servoNum,stepMIN[servoNum],stepMAX[servoNum], stepSize)
                      break
                   except ValueError:
                      print("No valid integer! Please try again ...")


          if command == 'n':
             backupFile(file)
             print ("Make a new task file name: (write name  without ext. press CR ")
             inputTerm = raw_input()
             if inputTerm == "q": #quit
                pass
             else:
                fileName = inputTerm
             file = dir + fileName + ext
             newProject(file)

          if command == 's':
             saveRobotData(file,NUMBERofSERVOS,servoPOS,delay)


          if command == 'o':
             print ("Open existing task file name: (write name without ext. press CR")
             inputTerm = raw_input()
             if inputTerm == "q": #quit
                pass
             else:
                fileName = inputTerm
                file = dir + fileName + ext

          if command == 'a':
             print ("Append task file to  excisting task file name: (write name without ext. press CR")
             inputTerm = raw_input()
             if inputTerm == "q": #quit
                pass
             else:
                fromFileName = inputTerm
                fromFile = dir + fromFileName + ext
                appendMoveData(file,fromFile)

          if command == 'r':
             print ("Run task in task file:", fileName+".mov")
             #goToZero(NUMBERofSERVOS,zeroANGLE)
             moveRobot(file,NUMBERofSERVOS, speed, zeroANGLE)

          if command == 'rc':
             print ("Run task fil cycle by cyckle:", fileName+".mov")
             #goToZero(NUMBERofSERVOS,zeroANGLE)
             moveCycleByCyckle(dir,fileName,file,NUMBERofSERVOS, speed, zeroANGLE)

          if command == 't':
             print ("Set new speed time (0.99 - 0.0001):",speed)
             value = float(raw_input())
             if value >= 0.0001 and value <= 0.99:
                speed = value

          if command == 'd':
             print ("Set new  delay between cycles (0.0 - 100.0):",delay)
             value = float(raw_input())
             if value >= 0.0 and value <= 100.0:
                delay = value

          if command == 'l':
             print ("List movement data in task file:",fileName+".mov")
             listMoveData(file)

          if command == 'v':
             startInfo(version,versiondate)
             print ("        VERSION SETUP DATA")
             print ("Program version             :",version)
             print ("Version date                :",versiondate)
             print ("Task file name              :",fileName+".mov")
             print ("Directory and file name     :",file)
             print ("Programming step size count :",stepSize)
             print ("Delay between task cycles   :",delay)
             print ("Running speed time          :",speed)
             print ("Number of servos            :",NUMBERofSERVOS)

          if command == 'z':
             print ("Go to zero position")
             goToZero(NUMBERofSERVOS,zeroANGLE)

          if command == 'f':
             print ("Show task files  (*.mov):")
             showTaskFiles()

          if command == 'h':
             print ("      HELP - COMMAND MENU")
             print ("Make a new task file            : n")
             print ("Open an existing task file      : o")
             print ("Programming mode for servos     : p")
             print ("Select servo 1 - x to move      : 1 - x")
             print ("Save movement cycle in task file: s")
             print ("List movement data in task file : l")
             print ("Append move data in task file   : a")
             print ("Run task in task file           : r")
             print ("Run cycle by cycle in task file : rc")
             print ("Show task files (*.mov)         : f")
             print ("Increase step                   : +")
             print ("Decrease step                   : 0")
             print ("Set step size count             : c")
             print ("Set new movement speed time     : t")
             print ("Set new cycle delay              : d")
             print ("Go to zero position             : z")
             print ("Show version setup data         : v")
             print ("Show servo numbers              : nu")
             print ("Help                            : h")
             print ("Exit                            : q")


          if command == 'nu':
             robotDraw(dFile)


          if command == 'test':
             print ("Test")
             test(NUMBERofSERVOS)
             print (file)



if __name__ == "__main__":

    init()

    controlModule()
