import math
import cv2
#######   some poker deskew func #########
def getfirstx(im,index=0,start='up',order=1):
    if start == 'up':
        pass
    elif start == 'down':
        index = im.shape[0] - 1 - index

    count = 0
    for point in im[index, : : order]:
        if point == 255:
            if order == 1:
                return float(count)
            elif order == -1:
                return float(im.shape[1] - count)
        count += 1
    return 0
        
def getfirsty(im,index=0,start='left',order=1):
    if start == 'left':
        pass
    elif start == 'right':
        index = im.shape[1] - 1 - index

    count = 0
    for point in im[ : : order,index]:
        if point == 255:
            if order == 1:
                return float(count)
            elif order == -1:
                return float(im.shape[0] - count)
        count += 1
    return 0
        
def getdeskewanglefromleftuptriangle(im):
    times = 3
    degrees = 0
    for time in range(times):
        x = getfirstx(im,time,'up',1)
        y = getfirsty(im,time,'left',1)
        
        if (x < 30) or (y < 30):
            return -1
        #if not y==0:
        ratio = x / y
        degree = math.degrees(math.atan(ratio))
        #print degree
        degrees += degree
    return degrees / times
    
def getdeskewanglefromrightdowntriangle(im):
    times = 3
    degrees = 0
    for time in range(times):
        x = im.shape[1] - getfirstx(im,time,'down',-1)
        y = im.shape[0] - getfirsty(im,time,'right',-1)
        
        if (x< 30) or (y < 30):
            return -1
        #if not y==0:
        ratio = x / y
        degree = math.degrees(math.atan(ratio))
        #print degree
        degrees += degree
    return degrees / times
    
def getdeskewangle(im):
    lu = getdeskewanglefromleftuptriangle(im)
    if not lu == -1:
        #print "1 : ",lu
        return lu
    else:
        rd = getdeskewanglefromrightdowntriangle(im)
        #print "2 : ",rd
        return rd
        
#source : http://stackoverflow.com/questions/11764575/python-2-7-3-opencv-2-4-after-rotation-window-doesnt-fit-image    
def rotateImage(image, angel):#parameter angel in degrees
    height = image.shape[0]
    width = image.shape[1]
    height_big = height * 2
    width_big = width * 2
    image_big = cv2.resize(image, (width_big, height_big))
    image_center = (width_big/2, height_big/2)#rotation center
    rot_mat = cv2.getRotationMatrix2D(image_center,angel, 0.5)
    result = cv2.warpAffine(image_big, rot_mat, (width_big, height_big), flags=cv2.INTER_LINEAR)
    return result
    
def rotateImage2(image, angel):#parameter angel in degrees
    height = image.shape[0]
    width = image.shape[1]
    height_big = height * 4
    width_big = width * 4
    image_big = cv2.resize(image, (width_big, height_big))
    image_center = (width_big/2, height_big/2)#rotation center
    rot_mat = cv2.getRotationMatrix2D(image_center,angel, 0.25)
    result = cv2.warpAffine(image_big, rot_mat, (width_big, height_big), flags=cv2.INTER_LINEAR)
    return result
    
##########################################