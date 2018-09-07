
import RPi.GPIO as GPIO
from time import sleep, time

#GPIO Pins --- PWM for motors
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT) #output mode
fork = GPIO.PWM(18, 50) #fork lift motors PWM pin at 50Hz Frequency
#-----

#PWM for Servo Motors (SG90) -
# position "0" [degrees] (~1.5 ms pulse) is middle
# position "90" [decrees] (~2ms pulse) is all the way to the right
# position "-90" [degrees] (~1ms pulse) is all the way to the left

#TODO: Do we need to calculate different with 0.02s (20ms) vs 20(s)
dc0 = 0.05 #1 / 20
dcSub90 = 0.075 #1.5 / 20
dc90 = 0.1 #2 / 20


def forkMotor():
    fork.start(0)
    fork.ChangeDutyCycle(dc0)
    time.sleep(1)  # 1s
    fork.ChangeDutyCycle(dcSub90)
    time.sleep(1)  # 1s
    fork.ChangeDutyCycle(dc0)
    time.sleep(1)  # 1s
    fork.ChangeDutyCycle(dc90)
    fork.stop()

for x in range(0, 10):      #loop for 10
    forkMotor()