#!/usr/bin/env python
#source:http://opencv-code.com/quick-tips/take-snapshot-from-your-webcam/
"""
webcam-snapshot.py:
A simple tool for taking snapshots from webcam. The images are saved in the 
current directory named 1.jpg, 2.jpg, ...

Usage:
    Press [SPACE] to take snapshot
    Press 'esc' to quit
"""

#default value
symbol = 'spade'
number = '1'

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

    if key == ord(' '):
      t0 = cv2.getTickCount()
      take_picture = True
    elif key in keysOfPokerNumber :
      filenum = 1
      if key in number0to9:
        if key == 48 :
          number = str(10)
        else :
          number = str(key-48).zfill(2)
      elif key in j :
        number = '11'
      elif key in q :
        number = '12'
      elif key in k :
        number = '13'
      print 'filenum initial.'
      print 'number : ', number
    elif key in keysOfPokerSymbol :
      filenum = 1
      if key in spade:
        symbol = 'spade'
      elif key in heart :
        symbol = 'heart'
      elif key in diamond :
        symbol = 'diamond'
      elif key in club :
        symbol = 'club'
      print 'filenum initial.'
      print 'symbol : ', symbol

    elif key == 27:
      break

    if take_picture and ((cv2.getTickCount()-t0) / cv2.getTickFrequency()) > delay:
      print 'save pic : ' + 'training data//' + symbol + '//' + number + '-' + str(filenum).zfill(2) + ".jpg"
      #cv2.imwrite(str(filenum) + ".jpg", frame)
      cv2.imwrite('training data//' + symbol + '//' + number + '-' + str(filenum).zfill(2) + ".jpg", frame)
      filenum += 1
      take_picture = False

  cap.release()

if __name__ == "__main__":
  take_snapshot()