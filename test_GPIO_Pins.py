import GPIO

#Init GPIO Pins
#three pins (used for a binary sequence) as an output, which is connected to the bluepill
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT) # 00x - lsb

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT) # 0x0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25, GPIO.OUT) # x00 - msb

# handshake between bluepill
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT) # instruct bluepill to do commands

GPIO.setmode(GPIO.BCM) # signal that bluepill is done with movement command
GPIO.setwarnings(False)
GPIO.setup(27, GPIO.IN) # will expect that blupill will set the pin back to low

#functions
def backward():
    GPIO.output(17, GPIO.LOW)  # reset the handshake between bluepill and pi
    if GPIO.input(27, GPIO.HIGH):
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.HIGH)

        GPIO.output(17, GPIO.HIGH)
        return

def forward():
    GPIO.output(17, GPIO.LOW)  # reset the handshake between bluepill and pi
    if GPIO.input(27, GPIO.HIGH):
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(25, GPIO.LOW)

        GPIO.output(17, GPIO.HIGH)
        return

def left():
    GPIO.output(17, GPIO.LOW)  # reset the handshake between bluepill and pi
    if GPIO.input(27, GPIO.HIGH):
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)

        GPIO.output(17, GPIO.HIGH)
        return

def right():
    GPIO.output(17, GPIO.LOW)  # reset the handshake between bluepill and pi
    if GPIO.input(27, GPIO.HIGH):
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(25, GPIO.HIGH)

        GPIO.output(17, GPIO.HIGH)
        return

#main function (aka beef of test program)

#validate each command works
forward() # one forward command
right() # rotate right
backward() # one backward command
left() # rotate left

#square movement
for x in range(0, 3):
    GPIO.output(17, GPIO.LOW)
    forward()
    GPIO.output(17, GPIO.LOW)
    right()
