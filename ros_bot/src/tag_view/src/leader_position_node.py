#!/usr/bin/python3.7

import rospy
import cv2
import math

from std_msgs.msg import Int16MultiArray
from pyzbar import pyzbar

SCALE = 1/4

#camera v2
#QR_H_PIXEL = 1400

#camera v1
QR_H_PIXEL = 810

QR_H_MM = 50 #QR heigth of the qr-code in mm
REF_DISTANCE = 100

k = QR_H_PIXEL*SCALE/QR_H_MM #index for converting from pixels to mm
FOCAL_LENGTH = REF_DISTANCE*k #focal lenght in pixeles

#camera v2
#frame_x = int(3280 * SCALE)
#frame_y = int(2464 * SCALE)

#camera v1 noIR
frame_x = int(2592 * SCALE)
frame_y = int(1944 * SCALE)

dim = (frame_x, frame_y)

# center coordinates of the frame
xc = frame_x/2
yc = frame_y/2

def scan():

    position = Int16MultiArray()  # array for the distance and angle

    rospy.init_node('get_leader_node') # initializftion of the node
    pub = rospy.Publisher('/leader_position', Int16MultiArray, queue_size = 1) # publisher creation

    rospy.loginfo("Ready to scan")  # command line info

    cap = cv2.VideoCapture(0)   # get the video stream

    '''working with the video stream'''
    while not rospy.is_shutdown():

        _, frame = cap.read()   # get the image from the video stream

        frame = cv2.resize(frame, dim)   #resizing

        barcodes = pyzbar.decode(frame)     # decoding of the image

        '''working with qr-code in the image'''
        if len(barcodes) > 0:   # check if the image includes qr-code


            for barcode in barcodes:

                (x, y, w, h) = barcode.rect     # coordinates and size of the qr-code
                #print(h,w)  #for test qr code size in pixeles
                x0 = (-xc + x + w/2)/k      # x coordinate
                #y0 = (yc - y - h/2)*100/k      # y coordinate
                z0 = FOCAL_LENGTH*QR_H_MM/h      # z coordinate

                #distance = int(math.sqrt(xp*xp + yp*yp + z0*z0))    #distance between the camera and the object in meters
                distance = math.sqrt(x0*x0 + z0*z0)   # 2d distance
                angle = math.atan(x0/z0)*180/math.pi    # angle between the center axis and qr-code
                position.data = [int(distance), int(angle)]   # final package for publishing

        elif len(barcodes) == 0:    # if no qr-code, will publish constant value

            position.data = [-1]

        pub.publish(position)   # publishing the position to the topic /leader_position


if __name__ =='__main__':
    try:
        scan()
    except rospy.ROSInterruptException:
        pass