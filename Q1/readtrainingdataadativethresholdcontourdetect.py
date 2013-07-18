import os
import cv2
import Image
import numpy as np
from datetime import datetime 
from matplotlib import pyplot as plt

numbers = [str(i).zfill(2) for i in range(1,14)]
symbols = ['spade' , 'heart' , 'diamond' , 'club']

for symbol in symbols:
    for dirPath, dirNames, fileNames in os.walk(os.path.join('training data',symbol)):
        for f in fileNames:
            filename = os.path.join(dirPath, f)
            print filename

            im = cv2.imread(filename)
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray,5)
            #gray = cv2.bilateralFilter(gray,5,10,10)
            #cv2.imshow('imf',gray)
            thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,3)
            cv2.imshow('th',thresh)
            #contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cv2.imshow('th1',thresh)
            print hierarchy
            for cnt in contours:
                #if (1500 < cv2.contourArea(cnt)) and (cv2.contourArea(cnt)<10000):
                if (100 < cv2.contourArea(cnt)):
                #if (100 < cv2.contourArea(cnt)) and (cv2.contourArea(cnt)<1000):
                    [x,y,w,h] = cv2.boundingRect(cnt)
                    
                    #if(cv2.contourArea(cnt)<250) :                   #it is small symbol
                        #if (24<w)or(24<h):
                            #break
                        #if (15>w)or(15>h):
                            #break
                    #elif(400 < cv2.contourArea(cnt)) :               #it is number
                        #if (50<w)or(50<h):
                            #break
                        #if (24>w)or(24>h):
                            #break
                    
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.cv.BoxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(im,[box],0,(255,0,0),2)
                    print cv2.contourArea(cnt),cv2.boundingRect(cnt)," : "
                    #print box
                    
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(10,10))
                    roismall = roismall.reshape((1,100))
                    roismall = np.float32(roismall)
                    #retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
                    #string = str(int((results[0][0])))
                    #cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
            
            cv2.imshow('im',im)
            key = cv2.waitKey(-1)

            if key == ord(' '):
                continue