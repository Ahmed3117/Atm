'''import cv2
import numpy as np
from pyzbar.pyzbar import decode
img=cv2.imread('first.png')
code=decode(img)
print(code[0].data.decode('ascii'))
'''
'''
import pyqrcode
qr=pyqrcode.create('ahmed issa')
qr.png('first.png',scale=8)
'''



    
import cv2
import numpy as np
from pyzbar.pyzbar import decode
#img=cv2.imread('first.png')
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
filterdata=set()
while True:
    mydata=''
    sucsess,img=cap.read()
    for barcode in decode(img):
        mydata=barcode.data.decode('utf-8')
        filterdata.add(mydata)
        
    cv2.imshow('result',img)
    cv2.waitKey(1)
print(filterdata)

'''
import cv2
import numpy as np
from pyzbar.pyzbar import decode
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
mydata=''
count=0
while True:
    sucsess,img=cap.read()
    for barcode in decode(img):
        mydata=barcode.data.decode('utf-8')
        print(mydata)
        count+=1
    if count==1:
        cap.release()
        cv2.destroyAllWindows()
        break
    cv2.imshow('result',img)
    cv2.waitKey(1)
'''
