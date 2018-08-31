# from Tkinter import Image
from PIL import Image, ImageOps
import RPi.GPIO as GPIO
import time
import PIL.ImageOps
# from PIL import zbarlight

import webbrowser
import zbarlight
import picamera
from time import sleep
import pygame

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT) #Pi pin 14 connects to CEENBoT pin 14 (PD2)

#Wait
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.OUT) #output mode

#PWM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT) #output mode
pwm = GPIO.PWM(18, 100) #PWM pin at 100Hz Frequency - necessary?

#movement commands
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT) #output mode (LSB)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(15, GPIO.OUT) #output mode (MSB)

WIDTH = 1280
HEIGHT = 1024
qr_found = False

sleep(5)

# INIT CAMERA
camera = picamera.PiCamera()
camera.vflip = False
camera.hflip = False
camera.brightness = 60

# BUILD A SCREEN
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
black = pygame.Color(0, 0, 0)
textcol = pygame.Color(255, 255, 0)
screen.fill(black)

#continuously take a picture
while True:
	#conditional if only needed to take one qr code image
	#while( qr_found == False ):
		
		# TAKE A PHOTO
		camera.start_preview()
		sleep(2)
		camera.capture('/home/pi/imageProcessing/potentialQRCode.png', format='png')
		screen.fill(black)
		pygame.display.update()
		camera.stop_preview()

		# READ IMAGE AND PUT ON SCREEN
		img = pygame.image.load('/home/pi/imageProcessing/potentialQRCode.png')
		screen.blit(img, (0, 0))

		#files = 'potentialQRCode.png'
		files = '/home/pi/imageProcessing/potentialQRCode.png'
		image = open(files, 'rb')
		with image:
			image = Image.open(image)
			image.load()
		codes = zbarlight.scan_codes('qrcode', image)
		
		#cannot find qr code
		if codes == None:				
			image = Image.open(files)
			
			#converts image to black and white
			image = image.convert('L')
			
			#inverts the image
			image1 = ImageOps.invert(image)
			image1.save('/home/pi/imageProcessing/potentialQRCode.png')
			
			files1 = '/home/pi/imageProcessing/potentialQRCode.png'
			image1 = open(files1, 'rb')
			#checks again for a qr code
			with image1:
				image1 = Image.open(image1)
				image1.load()

			codes = zbarlight.scan_codes('qrcode', image1)
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
			
		image = Image.open('/home/pi/imageProcessing/potentialQRCode.png')

# Will never be reached to avoid opening many browsers		
urlCode = ', '.join(codes)
webbrowser.open(urlCode, new=2)
print('QR codes: %s' % codes)
sleep(3)

#_________			
			#where to implement PWM?
			dc = 0
			pwm.start(dc)
			for dc in range (50):
				pwm.ChangeDutyCycle(dc) #necessary to change duty cycle?
				time.sleep(0.002) #2ms 
				
			pwm.stop()
#__________

pygame.quit()
