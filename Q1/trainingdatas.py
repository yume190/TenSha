import numpy as np
import cv2
import os
import sys

from edge import *
from deskew import *
from corner import *
from keyvalue import *

#######   some lambda func ###############
l = lambda s: cv2.boundingRect(s)[0]
r = lambda s: cv2.boundingRect(s)[0] + cv2.boundingRect(s)[2]
u = lambda s: cv2.boundingRect(s)[1]
d = lambda s: cv2.boundingRect(s)[1] + cv2.boundingRect(s)[3]
##########################################

def getcornerimage(imgrotate):
    t1 = imgrotate[cornerup:cornerdown,cornerleft:cornerright]
    t2 = imgrotate[cornerleft:cornerright,acornerdown:acornerup]
    t3 = imgrotate[acornerright:acornerleft,cornerup:cornerdown]
    t4 = imgrotate[acornerdown:acornerup,acornerright:acornerleft]
    #t2 = t2.T[::-1,:]
    #t3 = t3.T[:,::-1]
    #t4 = t4[::-1,::-1]
    t2 = rotateImage2(t2,90)#[30:130,180:220]
    t3 = rotateImage2(t3,270)#[30:130,180:220]
    t4 = rotateImage(t4,180)#[50:150,20:60]
    t2 = t2[0.5 * t2.shape[0] - 0.5 * (cornerdown - cornerup):0.5 * t2.shape[0] + 0.5 * (cornerdown - cornerup),0.5 * t2.shape[1] - 0.5 * (cornerright - cornerleft):0.5 * t2.shape[1] + 0.5 * (cornerright - cornerleft)]
    t3 = t3[0.5 * t3.shape[0] - 0.5 * (cornerdown - cornerup):0.5 * t3.shape[0] + 0.5 * (cornerdown - cornerup),0.5 * t3.shape[1] - 0.5 * (cornerright - cornerleft):0.5 * t3.shape[1] + 0.5 * (cornerright - cornerleft)]
    t4 = t4[0.5 * t4.shape[0] - 0.5 * (cornerdown - cornerup):0.5 * t4.shape[0] + 0.5 * (cornerdown - cornerup),0.5 * t4.shape[1] - 0.5 * (cornerright - cornerleft):0.5 * t4.shape[1] + 0.5 * (cornerright - cornerleft)]
    return t1,t2,t3,t4
    
def issymbol(x,y,w,h,area):
    if(area<450) :                   #it is small symbol
        if (17<h)and(h<28):
            if (15<w)and(w<30):
                return True
    return False
    
def isnumber(x,y,w,h,area):
    if(y+h) > 80:
        return False
    if(350<area) :                   #it is small symbol
        #if (20<h)and(h<60):
            #if (15<w)and(w<30):
        return True
    return False

#######   training part    ############### 
samples = np.loadtxt('generalsamples.data',np.float32)
responses = np.loadtxt('generalresponses.data',np.float32)
#responses = responses.reshape((responses.size,1))

responses = responses.tolist()
#samples =  np.empty((0,100))

symbols = ['spade' , 'heart' , 'diamond' , 'club']
for symbol in symbols:
    for dirPath, dirNames, fileNames in os.walk(os.path.join('training data',symbol)):
        for f in fileNames:
            filename = os.path.join(dirPath, f)
            print filename
            
            im = cv2.imread(filename)
            out = np.zeros(im.shape,np.uint8)
            img = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
            img = cv2.medianBlur(img,5)
            img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,1,11,3)
            
            img = cutpoker(img)
            angel = getdeskewangle(img)
            imgrotate = rotateImage(img,angel)
            imgrotate = cutpoker(imgrotate)

            targets = [t1,t2,t3,t4] = getcornerimage(imgrotate)
            
            #################      Now finding Contours         ###################
            
            for target in targets:
                show  = target.copy()
                contours,hierarchy = cv2.findContours(target,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

                #contours.sort(key = l)
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if (100 < area) and (area<1200):
                        [x,y,w,h] = cv2.boundingRect(cnt)
                        
                        if not (isnumber(x,y,w,h,area) or issymbol(x,y,w,h,area)):
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
                            responses = np.array(responses,np.float32)
                            responses = responses.reshape((responses.size,1))
                            np.savetxt('generalsamples.data',samples)
                            np.savetxt('generalresponses.data',responses)
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
responses = responses.reshape((responses.size,1))
print "training complete"

np.savetxt('generalsamples.data',samples)
np.savetxt('generalresponses.data',responses)