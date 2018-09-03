# from Tkinter import Image
from PIL import Image, ImageOps
import RPi.GPIO as GPIO
# from PIL import zbarlight

import webbrowser
import zbarlight
import picamera
from time import sleep
import pygame

#-----GPIO Pins
#Wait
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.OUT) #output mode- tells bluepill to perform tasks

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(3, GPIO.IN) #input mode- bluepill tells pi when to perform task

#PWM for motors
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT) #output mode
fork = GPIO.PWM(18, 50) #fork lift motors PWM pin at 50Hz Frequency

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
camera = GPIO.PWM(12, 50) #camera motor PWM pin at 50Hz Frequency

#movement commands
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT) #output mode (LSB)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(15, GPIO.OUT) #output mode (MSB)

#------





def initCamera():
    global camera
    camera = picamera.PiCamera()
    camera.vflip = False
    camera.hflip = False
    camera.brightness = 60

def BuildAScreen():
	global screen, black
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	black = pygame.Color(0, 0, 0)
	textcol = pygame.Color(255, 255, 0)
	screen.fill(black)


# BuildAScreen() - not necessary right now
def imageProcessing():
	global image, codes
	image = Image.open(files)
	# converts image to black and white
	image = image.convert('L')
	# inverts the image
	image1 = ImageOps.invert(image)
	image1.save('/home/pi/imageProcessing/potentialQRCode.png')
	files1 = '/home/pi/imageProcessing/potentialQRCode.png'
	image1 = open(files1, 'rb')
	# checks again for a qr code
	with image1:
		image1 = Image.open(image1)
		image1.load()
	codes = zbarlight.scan_codes('qrcode', image1)

WIDTH = 1280
HEIGHT = 1024
qr_found = False

sleep(5)

initCamera()

#continuously take a picture
while True:
	#conditional if only needed to take one qr code image
	#while( qr_found == False ):
		
		# TAKE A PHOTO
		camera.start_preview()
		sleep(2) # potentially reduce time
		camera.capture('/home/pi/imageProcessing/potentialQRCode.png', format='png')
		#screen.fill(black)
		#pygame.display.update()
		#camera.stop_preview()

		# READ IMAGE AND PUT ON SCREEN
		#img = pygame.image.load('/home/pi/imageProcessing/potentialQRCode.png')
		#screen.blit(img, (0, 0))

		files = '/home/pi/imageProcessing/potentialQRCode.png'

		image = open(files, 'rb')
		with image:
			image = Image.open(image)
			image.load()
		codes = zbarlight.scan_codes('qrcode', image)
		
		#cannot find qr code
		#if codes == None:
		#	imageProcessing()
		# necessary to check that code
		if (codes != None):
			qr_found = True
			print "QR Code Found"
			
			#TODO: check if qr code matches 
			#various row/column of warehouse
			 
			GPIO.output(14, GPIO.HIGH)
			#if (codes == '[\'http://qrs.ly/bn6pa5j\']'):     # QR code 1
				#GPIO.output(14, GPIO.HIGH)
				#print "Pin 14 is HIGH"
			#elif (codes == '[\'http://qrs.ly/2h6pj9c\']'):   # QR code 2
				#GPIO.output(14, GPIO.LOW)
				#print "Pin 14 is LOW"
		else:
			print "QR Code NOT Found"
			GPIO.output(14, GPIO.LOW)
			
		#image = Image.open('/home/pi/imageProcessing/potentialQRCode.png')

# Will never be reached to avoid opening many browsers		
urlCode = ', '.join(codes)
webbrowser.open(urlCode, new=2)
print('QR codes: %s' % codes)
sleep(3)

#_________			
# used when the correct location for the crate is to be placed

dc0 = 0.05 #1 / 20ms
dcSub90 = 0.075 #1.5 / 20ms

fork.start(dc)
fork.ChangeDutyCycle(dc)
time.sleep(0.002)  # 2ms
fork.stop()

camera.start(dc)
camera.ChangeDutyCycle(dc)
time.sleep(0.002)  # 2ms
camera.stop()
#__________

pygame.quit()
