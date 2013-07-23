from matplotlib import pyplot as plt
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
def getleftedge(im):
    count = 0
    for point in im.sum(axis=0): 
        if point > (255*5):
            return count
        count += 1

def getrightedge(im):
    count = 0
    for point in im.sum(axis=0)[ : :-1]:                                 # reversed im
        if point > (255*5):
            return im.shape[1] - count
        count += 1

def getupedge(im):
    count = 0
    for point in im.sum(axis=1):
        if point > (255*5):
            return count
        count += 1
    
def getdownedge(im):
    count = 0
    for point in im.sum(axis=1)[ : :-1]:
        if point > (255*5):
            return im.shape[0] - count
        count += 1
 ###############################################################################################       
def getleftedge2(im,mid):
    count = 0
    for point in im.sum(axis=0)[ : mid : -1]: 
        if point == 0 :
            return mid - 1 - count
        count += 1
    return 0

def getrightedge2(im,mid):
    count = 0
    for point in im.sum(axis=0)[ mid : : 1]:                                 # reversed im
        if point == 0:
            return mid + count
        count += 1
    return im.shape[1]

def getupedge2(im,mid):
    count = 0
    for point in im.sum(axis=1)[ : mid : -1]:
        if point == 0:
            return mid - 1 - count
        count += 1
    return 0
    
def getdownedge2(im,mid):
    count = 0
    for point in im.sum(axis=1)[ mid : : 1]:
        if point == 0:
            return mid + count
        count += 1
    return im.shape[0]
        
def cutpoker(im):
    #r = range(len(im.sum(axis=1)))
    #t = im.sum(axis=1)
    #plt.bar(r,t)
    #plt.show()
    a0=im.sum(axis=0)
    a1=im.sum(axis=1)
    m0,m1=a0.argmax(),a1.argmax()
    pokerleft = getleftedge(im)
    pokerright = getrightedge(im)
    pokerup = getupedge(im)
    pokerdown = getdownedge(im)
    return im[pokerup:pokerdown,pokerleft:pokerright]

##########################################