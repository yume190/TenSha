import math
import cv2
from numpy import *
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
    if order == 1:
        return 0.0
    elif order == -1:
        return float(im.shape[1])
       
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
    if order == 1:
        return 0.0
    elif order == -1:
        return float(im.shape[0])  

#########################   fail func   #########################
def getlengthx(im,index=0,start='up',order=1):
    if start == 'up':
        yorder = 1
        im = im[index, : : order][index: :yorder]
    elif start == 'down':
        yorder = -1
        im = im[index, : : order][ :index:yorder]
    else:
        return -1

    count = 0
    for point in im:
        if point == 255:
            return float(count)
        count += 1
    return 0.0
def getlengthy(im,index=0,start='left',order=1):
    if start == 'left':
        xorder = 1
        im = im[ : : order,index][index: :xorder]
    elif start == 'right':
        xorder = -1
        im = im[ : : order,index][ :index:xorder]
    else:
        return -1

    count = 0
    for point in im:
        if point == 255:
            return float(count)
        count += 1
    return 0.0
#################################################################
    
def getdeskewanglefromleftuptriangle(im):
    times = 5
    degrees = []
    for time in range(times):
        x = getfirstx(im,time,'up',1)
        y = getfirsty(im,time,'left',1)
        
        if (x < 30) or (y < 30):
            continue
        ratio = x / y
        degree = math.degrees(math.atan(ratio))
        degrees.append(degree)
    result = returndegree(degrees)
    return result
    
def getdeskewanglefromrightdowntriangle(im):
    times = 5
    degrees = []
    for time in range(times):
        x = im.shape[1] - getfirstx(im,time,'down',-1)
        y = im.shape[0] - getfirsty(im,time,'right',-1)
        
        if (x< 30) or (y < 30):
            continue
        ratio = x / y
        degree = math.degrees(math.atan(ratio))
        degrees.append(degree)
    result = returndegree(degrees)
    return result
    
def getdeskewanglefromrightuptriangle(im):
    times = 5
    degrees = []
    for time in range(times):
        x = im.shape[1] - getfirstx(im,time,'up',-1)
        y = getfirsty(im,time,'right',1)
        
        if (x< 30) or (y < 30):
            continue
        ratio = y / x
        degree = math.degrees(math.atan(ratio))
        degrees.append(degree)
    result = returndegree(degrees)
    return result
    
def getdeskewanglefromleftdowntriangle(im):
    times = 5
    degrees = []
    for time in range(times):
        x = getfirstx(im,time,'down',1)
        y = im.shape[0] - getfirsty(im,time,'left',-1)
        
        if (x< 30) or (y < 30):
            continue
        ratio = y / x
        degree = math.degrees(math.atan(ratio))
        degrees.append(degree)
    result = returndegree(degrees)
    return result
    
def returndegree(degrees):
    
    ave = average(array(degrees))
    std = array(degrees).std()
    lowerbound = ave - std
    upbound = ave + std
    lenangel = len(degrees)
    delangel = []    
    
    for degree in degrees:
        if (degree < lowerbound) or (upbound < degree):
            delangel.append(degree)
    for t in delangel:
        degrees.remove(t)
    #print degrees
    #print lowerbound,upbound
    
    #degrees.sort()
    #print degrees
    if lenangel == 5:
        #result = degrees[1] + degrees[2] + degrees[3]
        #return result / 3
        return average(array(degrees))
    elif lenangel == 4:
        #result = degrees[1] + degrees[2]
        #return result / 2
        return average(array(degrees))
    #elif len(degrees) == 3:
        #result = degrees[1]
        #return result
    #elif len(degrees) == 2:
        #result = degrees[0] + degrees[1]
        #return result / 2
    else:
        return -1
    
def getdeskewangle(im):
    lu = getdeskewanglefromleftuptriangle(im)
    rd = getdeskewanglefromrightdowntriangle(im)
    ld = getdeskewanglefromleftdowntriangle(im)
    ru = getdeskewanglefromrightuptriangle(im)
    angel = [lu,rd,ld,ru]
    angel.sort()
    
    for ang in range(angel.count(-1)):
        angel.remove(-1)

    #print angel
    #print average(array(angel)) - array(angel).std() , average(array(angel)) + array(angel).std()
    
    if len(angel) == 4 :
        return (angel[1] + angel[2]) / 2
    elif len(angel) == 3 :
        return angel[1]
    elif len(angel) == 2 :
        return (angel[0] + angel[1]) / 2
    elif len(angel) == 1 :
        return angel[0]
    else:
        return 0.0
        
    #if not lu == -1:
        #print "1 : ",lu
        #return lu
    #else:
        #print "2 : ",rd
        #return rd
        
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