import cv2
import Image
import numpy
from datetime import datetime 

def array2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = numpy.c_[arr, 255*numpy.ones((len(arr),1), numpy.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)

camera_port = 0
camera = cv2.VideoCapture(camera_port)

starttime = datetime.now() 
print 'start  time   : ' + str(starttime) 

retval, im = camera.read()
endtime = datetime.now()
print 'end  time   : ' + str(endtime) 
print 'total  time   : ' + str(endtime - starttime)
file = "image.jpg"
cv2.imwrite(file, im)
size = (640,480)
im = array2PIL(im,size)


endtime = datetime.now()
print 'end  time   : ' + str(endtime) 
print 'total  time   : ' + str(endtime - starttime)

del(camera)