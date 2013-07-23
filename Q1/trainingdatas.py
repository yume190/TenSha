import numpy as np
import cv2
import os
import sys

from edge import *
from deskew import *

#######   some lambda func ###############
l = lambda s: cv2.boundingRect(s)[0]
r = lambda s: cv2.boundingRect(s)[0] + cv2.boundingRect(s)[2]
u = lambda s: cv2.boundingRect(s)[1]
d = lambda s: cv2.boundingRect(s)[1] + cv2.boundingRect(s)[3]
##########################################

#some key value
j = [74,106] #key j J
q = [81,113] #key q Q
k = [75,107] #key k K
number0to9 = [i for i in range(48,58)] #key 0 to 9
spade = [85,115] #key s S
heart = [72,104] #key h H
diamond = [68,100] #key d D
club = [67,99] #key c C
keysOfPokerNumber = number0to9 + j + q + k
keysOfPokerSymbol = spade + heart + diamond + club
keys = keysOfPokerNumber + keysOfPokerSymbol

symbols = ['spade' , 'heart' , 'diamond' , 'club']

#######   training part    ############### 
#samples = np.loadtxt('generalsamples.data',np.float32)
#responses = np.loadtxt('generalresponses.data',np.float32)
#responses = responses.reshape((responses.size,1))

responses = []
samples =  np.empty((0,100))

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
            t1 = imgrotate[20:120,20:60]
            t2 = imgrotate[20:60,-120:-20]
            t3 = imgrotate[-60:-20,20:120]
            t4 = imgrotate[-120:-20,-60:-20]
            t2 = rotateImage2(t2,90)[30:130,180:220]
            t3 = rotateImage2(t3,270)[30:130,180:220]
            t4 = rotateImage(t4,180)[50:150,20:60]
            cv2.imshow('target1',t1)
            cv2.imshow('target2',t2)
            cv2.imshow('target3',t3)
            cv2.imshow('target4',t4)
            targets = [t1,t2,t3,t4]
            #targets = [t1]
            
            #################      Now finding Contours         ###################
            
            for target in targets:
                show  = target.copy()
                contours,hierarchy = cv2.findContours(target,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

                #contours.sort(key = l)
                for cnt in contours:
                    if (100 < cv2.contourArea(cnt)) and (cv2.contourArea(cnt)<1000):
                        [x,y,w,h] = cv2.boundingRect(cnt)
                        
                        if (w>50) or (h>50):
                            continue
                            
                        cv2.rectangle(show,(x,y),(x+w,y+h),255,2)
                        roi = target[y:y+h,x:x+w]
                        roismall = cv2.resize(roi,(10,10))
                        cv2.imshow('norm',im)
                        cv2.imshow('target1',t1)
                        cv2.imshow('target2',t2)
                        cv2.imshow('target3',t3)
                        cv2.imshow('target4',t4)
                        cv2.imshow('roi',show)
                        key = cv2.waitKey(0)

                        if key == 27:
                            sys.exit()
                        elif key in keys:
                            #responses.append(int(chr(key)))
                            responses.append(key)
                            sample = roismall.reshape((1,100))
                            samples = np.append(samples,sample,0)
                            #yume add this code
                            cv2.rectangle(show,(x,y),(x+w,y+h),0,2)
                        else:
                            cv2.rectangle(show,(x,y),(x+w,y+h),0,2)
                            pass
responses = np.array(responses,np.float32)
#responses = np.array(responses)
responses = responses.reshape((responses.size,1))
print "training complete"

np.savetxt('generalsamples.data',samples)
np.savetxt('generalresponses.data',responses)