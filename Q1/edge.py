from matplotlib import pyplot as plt
import numpy as np
#######   some poker edge func ###########
#def getleftedge(im):
    #count = 0
    #continuous = 0
    #for point in im.sum(axis=0):
        #if point > (255*5):
            #if continuous == 0:
                #target = count
            #elif continuous == 20:
                #return target
            #else:
                #continuous += 1
        #else:
            #continuous = 0
        #print point,count,continuous
        #count += 1
def getleftedge(im,thresh):
    count = 0
    for point in im.sum(axis=0): 
        if point > (255*thresh):
            return count
        count += 1

def getrightedge(im,thresh):
    count = 0
    for point in im.sum(axis=0)[ : :-1]:                                 # reversed im
        if point > (255*thresh):
            return im.shape[1] - count
        count += 1

def getupedge(im,thresh):
    count = 0
    for point in im.sum(axis=1):
        if point > (255*thresh):
            return count
        count += 1
    
def getdownedge(im,thresh):
    count = 0
    for point in im.sum(axis=1)[ : :-1]:
        if point > (255*thresh):
            return im.shape[0] - count
        count += 1
###############################################################################################       
def getleftedge2(im,thresh=95):
    points = im.sum(axis=0)
    for index,point in enumerate(points):
        if point > 0:
            nonzero = np.count_nonzero(points[index:index+100])
            if nonzero >= thresh:
                return index
    return 0

def getrightedge2(im,thresh=95):
    points = im.sum(axis=0)[ : :-1]
    for index,point in enumerate(points):
        if point > 0:
            nonzero = np.count_nonzero(points[index:index+100])
            if nonzero >= thresh:
                return im.shape[1] - index
    return im.shape[1]

def getupedge2(im,thresh=95):
    points = im.sum(axis=1)
    for index,point in enumerate(points):
        if point > 0:
            nonzero = np.count_nonzero(points[index:index+100])
            if nonzero >= thresh:
                return index
    return 0

def getdownedge2(im,thresh=95):
    points = im.sum(axis=1)[ : :-1]
    for index,point in enumerate(points):
        if point > 0:
            nonzero = np.count_nonzero(points[index:index+100])
            if nonzero >= thresh:
                return im.shape[0] - index
    return im.shape[0]
        
def cutpoker(im):
    #r = range(len(im.sum(axis=1)))
    #t = im.sum(axis=1)
    #plt.bar(r,t)
    #plt.show()
    #a0=im.sum(axis=0)
    #a1=im.sum(axis=1)
    #m0,m1=a0.argmax(),a1.argmax()
    #print a0
    #print a1
    thresh = 99
    pokerleft = getleftedge2(im,thresh)
    pokerright = getrightedge2(im,thresh)
    pokerup = getupedge2(im,thresh)
    pokerdown = getdownedge2(im,thresh)
    return im[pokerup:pokerdown,pokerleft:pokerright]

##########################################