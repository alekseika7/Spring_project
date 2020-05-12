#!/usr/bin/python3.7

from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2
import numpy as np

scale = 2500 # number of pixels in one meter
work_distance = 0.2 #distance (m) to count angle size of the qr-code
real_length = 0.04 #real lenght of the qr-code in meters
real_height = 0.04 #real heigth of the qr-code in meters 
real_angle_size = 2*np.arctan(real_length/(2*work_distance)) #angle size (rad) of the qr-code on 0.2 m distance 

print("video stream is running....")
vs = VideoStream(src=0).start()
time.sleep(2)

while True:
    
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    barcodes = pyzbar.decode(frame)
    
    for barcode in barcodes:
        
        #coordinates and size of qr-code
        (x, y, w, h) = barcode.rect
        
        #contour of the qr-code
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        #counting a distance between camera and qr-code 
        delta_w = np.abs(frame.shape[1]/2 - (x+w)/2) #center shift only in 'x' coordinate
        print(h)
        print(h/scale)
        distance = h/(scale*real_angle_size) #wrong!!!!! 
        print(round(distance,3))
        
        #converting data to string
        barcodeData = barcode.data.decode("utf-8")
        print(barcodeData)
        
          
    # show the output frame
    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
 
print("video stream is over...")
cv2.destroyAllWindows()
vs.stop()
