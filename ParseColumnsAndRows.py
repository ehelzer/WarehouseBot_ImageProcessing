from PIL import Image, ImageOps
import webbrowser
import zbarlight
import picamera
from time import sleep
import pygame

WIDTH = 1024
HEIGHT = 1024
qr_found = False

sleep(5)

# INIT CAMERA
camera = picamera.PiCamera()
camera.vflip = False
camera.hflip = False
camera.brightness = 70

# BUILD A SCREEN
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
black = pygame.Color(0, 0, 0)
textcol = pygame.Color(255, 255, 0)
screen.fill(black)

while True:
    camera.start_preview()
    sleep(.5)
    camera.capture('/home/pi/imageProcessing/parseQRCode.png', format='png')
    screen.fill(black)
    pygame.display.update()
    camera.stop_preview()

    # READ IMAGE AND PUT ON SCREEN
    img = pygame.image.load('/home/pi/imageProcessing/parseQRCode.png')
    screen.blit(img, (0, 0))

    # files = 'potentialQRCode.png'
    files = '/home/pi/imageProcessing/parseQRCode.png'
    image = open(files, 'rb')
    with image:
        image = Image.open(image)
        image.load()
    codes = zbarlight.scan_codes("qrcode", image)

    if (codes != None):
        qr_found = True
        #TODO: Error handling if the code does not have a coordinate
        print ('code: %s' % codes)
        [new_code.strip("[]") for new_code in codes]
        
        #find coordinates (column,row) inside qr object
        parts = new_code.split(',')
        column = parts[0]
        print ('Column: %s' %column)
        row = parts[1]
        print ('Row: %s' %row)
        #ready for the next qr code
        qr_found = False
        break
        
    else:
		#will continue to check for qr 
        print "QR Code NOT Found"
        
        
        
     
