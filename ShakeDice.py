#AllServoTest.py
# test code that ramps each servo from 0-180-0 
import PicoRobotics
import time


board = PicoRobotics.KitronikPicoRobotics()

for degrees in range(150):
    board.servoWrite(1, 150-degrees)
    time.sleep(0.01) #ramp speed over 10x180ms => approx 2 seconds.
for degrees in range(150):
    board.servoWrite(1, degrees)
    time.sleep(0.01) #ramp speed over 10x180ms => approx 2 seconds.

# Shake a bit
time.sleep(1.0)
board.servoWrite(1, 125)
time.sleep(0.2)
board.servoWrite(1, 180)
time.sleep(0.2)
board.servoWrite(1, 150)
time.sleep(5.0)
