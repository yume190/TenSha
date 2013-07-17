#!/usr/bin/env python
#source:http://opencv-code.com/quick-tips/take-snapshot-from-your-webcam/
"""
webcam-snapshot.py:
A simple tool for taking snapshots from webcam. The images are saved in the 
current directory named 1.jpg, 2.jpg, ...

Usage:
    Press [SPACE] to take snapshot
    Press 'q' to quit
"""

import cv2

def take_snapshot(delay=1):
  cap = cv2.VideoCapture(0)
  if not cap.isOpened():
    print "Cannot open camera!"
    return

  #Set video to 320x240
  #cap.set(3, 320) 
  #cap.set(4, 240)

  take_picture = False;
  t0, filenum = 0, 1

  while True:
    val, frame = cap.read()
    cv2.imshow("video", frame)

    key = cv2.waitKey(30)
    #key = cv2.waitKey(-1)

    if key == ord(' '):
      t0 = cv2.getTickCount()
      ####################################################
      print t0
      take_picture = True
    elif key == ord('q'):
      break

    if take_picture and ((cv2.getTickCount()-t0) / cv2.getTickFrequency()) > delay:
      print 'save pic' + str(filenum)
      cv2.imwrite(str(filenum) + ".jpg", frame)
      filenum += 1
      take_picture = False

  cap.release()

if __name__ == "__main__":
  take_snapshot()