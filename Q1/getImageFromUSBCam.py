#-*- coding: utf-8 -*-
from VideoCapture import Device
import Image
from datetime import datetime 

cam = Device()
starttime = datetime.now() 
print 'start  time   : ' + str(starttime) 
im = cam.getImage()
endtime = datetime.now()
print 'end  time   : ' + str(endtime) 
print 'total  time   : ' + str(endtime - starttime)

starttime = datetime.now() 
print 'start  time   : ' + str(starttime) 

width = 640
height = 480
size = (width, height)
im = im.resize( size, Image.BILINEAR )
im.save( "image/image.jpg", "JPEG" )

#for a in range(90):
#    im2 = im.rotate( a, Image.BILINEAR )
#    im2.save( "imager" + str(a) + ".jpg", "JPEG" )

im = im.convert('L') #轉成灰階
im.save( "image/image1.jpg", "JPEG" )
for i in range(im.size[0]):
    for j in range(im.size[1]):
        if(im.getpixel((i,j))>150):
            im.putpixel((i,j),255) #轉成純白
        else:
            im.putpixel((i,j),0)   #轉成純黑
im.save( "image/image2.jpg", "JPEG" )

box = (200,20,250,150)
xim = im.crop(box)
xim.save( "image/imagex.jpg", "JPEG" )

endtime = datetime.now()
print 'end  time   : ' + str(endtime) 
print 'total  time   : ' + str(endtime - starttime)

"""
import cv2
import numpy as np

img = cv2.imread('imagex.jpg')
h = np.zeros((300,256,3))                                    # image to draw histogram

bins = np.arange(256).reshape(256,1)                         # Number of bins, since 256 colors, we need 256 bins
color = [ (255,0,0),(0,255,0),(0,0,255) ]

for ch,col in enumerate(color):
    hist_item = cv2.calcHist([img],[ch],None,[256],[0,256])  # Calculates the histogram
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX) # Normalize the value to fall below 255, to fit in image 'h'
    hist=np.int32(np.around(hist_item))                      
    pts = np.column_stack((bins,hist))                       # stack bins and hist, ie [[0,h0],[1,h1]....,[255,h255]]
    cv2.polylines(h,[pts],False,col)

h=np.flipud(h)                                               # You will need to flip the image vertically

cv2.imshow('colorhist',h)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""