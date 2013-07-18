import tesseract
import os

numbers = [str(i).zfill(2) for i in range(1,14)]
symbols = ['spade' , 'heart' , 'diamond' , 'club']

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetVariable("tessedit_char_whitelist", "0123456789abcdefghijklmnopqrstuvwxyz")
api.SetPageSegMode(tesseract.PSM_AUTO)





for symbol in symbols:
    for dirPath, dirNames, fileNames in os.walk(os.path.join('training data',symbol)):
        for f in fileNames:
            filename = os.path.join(dirPath, f)
            
            
            mImgFile = filename
            mBuffer=open(mImgFile,"rb").read()
            result = tesseract.ProcessPagesBuffer(mBuffer,len(mBuffer),api)
            print filename," : ",result