import os

numbers = [str(i).zfill(2) for i in range(1,14)]
symbols = ['spade' , 'heart' , 'diamond' , 'club']

for symbol in symbols:
    for dirPath, dirNames, fileNames in os.walk(os.path.join('training data',symbol)):
        #print dirPath
        for f in fileNames:
            print os.path.join(dirPath, f)