#!/usr/bin/python3.7

from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2

# initialize the video stream and allow the camera sensor to warm up
print("video stream is running....")
vs = VideoStream(src=0).start()
time.sleep(2)

# loop over the frames from the video stream
while True:
    
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
 
    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
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
