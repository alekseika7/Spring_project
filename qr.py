#!/usr/bin/python3.7

from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2
import numpy as np

REAL_WIDTH = 0.05 #real lenght of the qr-code in meters
REAL_HIGTH = 0.05 #real heigth of the qr-code in meters

#focal length was calculated using real object size (5x5 cm), distance = 10cm
#and height of the object in pixels (aprox. 200 pixels)
FOCAL_LENGTH = 400 
k = 4000 #index for converting from pixels to meters

print("video stream is running....")
vs = VideoStream(src=0).start()
time.sleep(2)

while True:
    
    frame = vs.read()
    frame = imutils.resize(frame, 700)
    xc, yc = int(frame.shape[1]/2), int(frame.shape[0]/2) #center coordinates of the frame
    cv2.line(frame, (xc, 0), (xc, yc*2), (128, 128, 128), 1)
    cv2.line(frame, (0, yc), (xc*2, yc), (128, 128, 128), 1)
    
    barcodes = pyzbar.decode(frame)  #all qr-codes in the frame
    
    for barcode in barcodes:
        
        #coordinates and size of the qr-code
        (x, y, w, h) = barcode.rect
        
        #get coordinates of the qr-code in center axis in cm
        x0 = round((-xc + x + w/2)*100/k, 3)     
        y0 = round((yc - y - h/2)*100/k, 3)   
        z0 = round(FOCAL_LENGTH*REAL_HIGTH*100/h, 3)
        
        distance = round(np.sqrt((x0/k)**2 + (y0/k)**2 + z0**2), 3)    #distance between the camera and the object in meters

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)    #frame of the qr-code
        cv2.putText(frame,
                    f"distance = {distance}",
                    (x, y-20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1)
        cv2.putText(frame,
                    f"x={x0}; y={y0}; z={z0}",
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1)
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
