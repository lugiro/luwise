LOS - LUWISE OPERATING SYSTEM
-----------------------------

User Manual v1.0
----------------

Content:
- Introduction
- Normal startup process
- Help Command menu
- Setup data
- Project specific startup values
- Hardware


Introduction
------------
LOS is a general control system for controlling several servos 
with Raspberry Pi and Servo PWM Pi expansion board from AB 
Electronics.

This is a command line program you can run from a terminal 
window. To start the program, write:<br>python losxxx.py
(xxx is the version number).

Before using the program look at the startup values shown in the 
function controlModule() in losxxx.py.<br> 
Also see the enclosed list. Most of the values are self-explanatory.

The program is set up for 32 servos. You will need two Servo PWM 
Pi expansion boards, with different board addresses. 

There are three main functions in the program:
1.	Move the servos to desired positions and save these 
positions in a task file
2.	Run the saved task file
3.	Fault handling and error correction

When running the program the servos will always rapibly go to the defined zero position,
 or angle 0, if not defined. Therefore when starting the program  with servos mounted on 
a robot, it can be an advantage to have the possibility to quickly cut the voltage 
to the servos. This can avoid damage on the robot.

When running the program the following text will appear:<br>New COMMAND:<br>


Normal startup process:
-----------------------
Press **n** to make a new task file for your project. You need to 
write a task file name, without extension. All task files are 
automatically given .mov as extension.

Next step is to press **p** for programming mode. Then you have to 
choose the servo you want to move, by number. This number will be 
the same number as you will find on the Servo PWM Pi expansion 
board. If you use two boards you will start with 17 on board 
number two.

You move the servo with **+** key in plus direction, and **0** for minus 
direction. The servos are set up to move from 0 to 250 steps 
(angle), but with restrictions set in the start up values, stepMIN and stepMAX. In your 
project you have to decide how to use this span.
To change the servo number, press CR and choose another number.
To quit the choose mode press **q**.

When you have made a cycle with several servo movements you can 
save this cycle with the command **s**. Between two cycles you can 
put a delay. With the command **d** you can change the delay. Default 
delay at startup is 0.

If you want to run your programmed task file press **r**. You will 
then be asked to go to zero position or not. Sometimes this can 
be useful and sometimes not. Hit y or n (or CR).
The servos shall now move to the same positions that you have 
programmed.

Sometimes you probably will be surprised. Because the servos will 
move simultaneously this can create movements that are difficult 
to foresee. Then it can be an advantage to have some tools for 
error detection.

If you use the command **rc** you can run the task file cycle by 
cycle. If you detect an error in the servo movement cycle you can 
write the command **save**. This will save the cycles before the 
error movement in the file c1.mov and save the cycles after the 
error in the file c2.mov. The error cycle will disappear.

Press **q** to quit and return to New COMMAND. Now you can press **n** to 
make a new empty task file and then append, with the command **a**, 
the file c1.mov to this empty file. Press **r** to run the file, then 
you can press **p** and start programming as described earlier.

After error correction and  new programming you can append 
the file c2.mov. Press **r** to run and test the new file.

There are also some useful commands for changing setup values.
The command **c** will change the step size for moving the servos in 
the programming mode. Default step value is 10. With a low step 
value there can be some problems when moving the servo with high 
torque.
The command **d** will set the delay (x.x sec) between two cycles. 
Default value is 0.

If you want to run your tasks faster or slower you can use the 
command **t** with value from 0.99 (very slow) to 0.0001 (fast). 
Default value is 0.01.

File handling command **l** will list the content in current task 
file. 
Use the command **v** to see, among other things, the name for the current task list.
The command **f** will list all the .mov files
The command **z** will return to the defined zero position.


HELP - COMMAND MENU
-------------------
Command h<br>
| **Command** | **Descrition** |
| n | make a new task file |
| o | open an existing task file |
| p | programming mode for servos |
|   | num - Select servo 1 - x to move, under command p |
| s | save movement cycle in task file |
| l | list movement data in task file |
| a | append move data in task file |
| r | run task in task file |
| rc | run cycle by cycle in task file |
|   | command save, saves cycles under command rc |
| f | show task files (*.mov) |
| c | set step size count |
|   | plus key   increase step, under command c |
|   | zero key   decrease step, under command c |
| t | set new movement speed time |
| d | set new cycle delay |
| z | go to zero position |
| v | show version setup data |
| nu | show servo numbers |
| h | help |
| q | exit/quit | 


SETUP DATA
----------
Command v
| **Description** | **Content** |
| Program version             : | version number |
| Version date                : | versiondate |
| Task file name              : | fileName |
| Directory and file name     : | file directory and filename |
| Programming step size count : | stepSize |
| Delay between task cycles   : | delay |
| Running speed time          : | speed |
| Number of servos            : | NUMBERofSERVOS |



Project specific startup values
-------------------------------
Values placed in the function controlModule() in losxxx.py<br>
| **Varable** | **Value** | **Description** |
| version | "2.00" | 
| versiondate | "23.06.2020"|
| NUMBERofSERVOS | 6 | number of servos in your project |
- stepSize = 10                (step size for programming servos)
- speed = 0.01                 (speed for running task)
- delay = 0.0                  (delay between task cycles)

- fileName = "task0"           (default task file name)
- ext = ".mov"                 (file extension for task file)
- dir = "/home/pi/RobotMan/"   (directory for files)
- file = dir + fileName + ext  (task file)
- drawFile = "robotDraw.txt"   (draw file with servo numbers)
- dFile = dir + drawFile

- servoPOS        (list of variable for actual servo position)
- stepMIN         (minimum allowed step/angle for each servo)
- stepMAX         (maximum allowed step/angle for each servo) 
- zeroANGLE       (defined zero position for servo) 


Hardware
--------
You will find all the necessary information about Servo PWM Pi 
expansion board on the AB Electronics websites. 
<br>Board addresses, how to download python modules etc.


IMPORTANT
--------
The servos should not have high torque for a long time 
(minutes). This will cause high current and damage the servos.
If you use a power supply with current measurement, you can
control the torque this way.

Feel free to use the program as you like. The program still has 
some errors and there are no warranties for the use. The 
developer of the LOS program has no responsibility for damage caused by
 the program and the servos. 


