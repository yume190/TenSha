#-*- coding: utf-8 -*-
from VideoCapture import Device
import Image

from datetime import datetime 
starttime = datetime.now() 
print 'start  time   : ' + str(starttime) 

cam = Device()
im = cam.getImage()
width = 640
height = 480
size = (width, height)
im = im.resize( size, Image.BILINEAR )
im.save( "image.jpg", "JPEG" )

#for a in range(90):
#    im2 = im.rotate( a, Image.BILINEAR )
#    im2.save( "imager" + str(a) + ".jpg", "JPEG" )

im = im.convert('L') #轉成灰階
im.save( "image1.jpg", "JPEG" )
for i in range(im.size[0]):
    for j in range(im.size[1]):
        if(im.getpixel((i,j))>150):
            im.putpixel((i,j),255) #轉成純白
        else:
            im.putpixel((i,j),0)   #轉成純黑
im.save( "image2.jpg", "JPEG" )

from pytesser import *
image = Image.open('image2.jpg')  # Open image object using PIL
print image_to_string(image)     # Run tesseract.exe on image

endtime = datetime.now()
print 'end  time   : ' + str(endtime) 
print 'total  time   : ' + str(endtime - starttime)
