import os
import sys

from edge import *
from deskew import *

import numpy as np
from datetime import datetime 

#######   training part    ############### 
samples = np.loadtxt('generalsamples.data',np.float32)
responses = np.loadtxt('generalresponses.data',np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.KNearest()
model.train(samples,responses)
##########################################

#######   some lambda func ###############
# input : contour
# output : contour (left/right/up/down)
l = lambda s: cv2.boundingRect(s)[0]
r = lambda s: cv2.boundingRect(s)[0] + cv2.boundingRect(s)[2]
u = lambda s: cv2.boundingRect(s)[1]
d = lambda s: cv2.boundingRect(s)[1] + cv2.boundingRect(s)[3]
##########################################

#######   some limit       ###############
max = 55
min = 13
filter = False
##########################################
numbers = [str(i).zfill(2) for i in range(1,14)]
symbols = ['spade' , 'heart' , 'diamond' , 'club']

for symbol in symbols:
    for dirPath, dirNames, fileNames in os.walk(os.path.join('training data',symbol)):
        for f in fileNames:
            filename = os.path.join(dirPath, f)
            print filename

            im = cv2.imread(filename)
            out = np.zeros(im.shape,np.uint8)
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            #gray = cv2.medianBlur(gray,5)
            gray = cv2.GaussianBlur(gray,(5,5),0)
            thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,1,11,3)
            
            img = cutpoker(thresh)
            angel = getdeskewangle(img)
            imgrotate = rotateImage(img,angel)
            imgrotate = cutpoker(imgrotate)
            
            cv2.imshow('cut',img)
            cv2.imshow('rotate',imgrotate)
            t1 = imgrotate[10:120,10:60]
            t2 = imgrotate[10:60,-120:-10]
            t3 = imgrotate[-60:-10,10:120]
            t4 = imgrotate[-120:-10,-60:-10]
            t2 = t2.T[::-1,:]
            t3 = t3.T[:,::-1]
            t4 = t4[::-1,::-1]
            cv2.imshow('target1',t1)
            cv2.imshow('target2',t2)
            cv2.imshow('target3',t3)
            cv2.imshow('target4',t4)
            print t1.sum(),t2.sum(),t3.sum(),t4.sum()
            targets = [t1,t2,t3,t4]
            
            #contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            contours,hierarchy = cv2.findContours(imgrotate.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            contours.sort(key = l)
            for cnt in contours:
                #if (1500 < cv2.contourArea(cnt)) and (cv2.contourArea(cnt)<10000):
                #if (10000 < cv2.contourArea(cnt)):
                if (100 < cv2.contourArea(cnt)) and (cv2.contourArea(cnt)<1000):
                    [x,y,w,h] = cv2.boundingRect(cnt)
                    
                    if filter:
                        if (w>max) or (h>max):
                            continue
                        if (w<min) or (h<min):
                            continue
                            
                        if(cv2.contourArea(cnt)<250) :                   #it is small symbol
                            if (24<w)or(24<h):
                                continue
                            if (15>w)or(15>h):
                                continue
                                
                        #elif(400 < cv2.contourArea(cnt)) :               #it is number
                            #if (50<w)or(50<h):
                                #continue
                            #if (24>w)or(24>h):
                                #continue
                    
                    #box contour
                    #rect = cv2.minAreaRect(cnt)
                    #box = cv2.cv.BoxPoints(rect)
                    #box = np.int0(box)
                    #cv2.drawContours(im,[box],0,(255,0,0),2)
                    
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(10,10))
                    roismall = roismall.reshape((1,100))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
                    string = str(int((results[0][0])))
                    cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
            
            cv2.imshow('im',im)
            #cv2.imshow('out',out)
            
            key = cv2.waitKey(-1)

            if key == 27:
                sys.exit()
    
cv2.destroyAllWindows()