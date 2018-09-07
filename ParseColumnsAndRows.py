from PIL import Image, ImageOps
import webbrowser
import zbarlight
import picamera
from time import sleep
import pygame

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

while True:
    camera.start_preview()
    sleep(2)
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
    codes = zbarlight.scan_codes('qrcode', image)

    if (codes != None):
        qr_found = True
        #find coordinates (column,row) inside qr object
        parts = codes.split(",")
        column = parts[0]
        row = parts[1]

    else:
        print "QR Code NOT Found"
