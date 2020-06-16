#!/usr/bin/python3.7

import rospy
from std_msgs.msg import Float32MultiArray

import cv2
from pyzbar import pyzbar
import numpy as np

REAL_WIDTH = 0.05   # real lenght of the qr-code in meters
REAL_HIGTH = 0.05   # real heigth of the qr-code in meters

# focal length was calculated using real object size (5x5 cm), distance = 10cm
# and height of the object in pixels (aprox. 200 pixels)
FOCAL_LENGTH = 400 
k = 4000    # index for converting from pixels to meters

'''main fucntion'''
def scan():

    position = Float32MultiArray()  # array for the distance and angle

    rospy.init_node('get_leader_node')  # initializftion of the node
    pub = rospy.Publisher('/leader_position', Float32MultiArray, queue_size = 1)    # publisher creation

    rospy.loginfo("Ready to scan")  # command line info 

    cap = cv2.VideoCapture(0)   # get the video stream
    
    '''working with the video stream'''
    while not rospy.is_shutdown():

        _, frame = cap.read()   # get the image from the video stream

        frame = cv2.resize(frame, (375, 500))   # resizing 
        xc, yc = frame.shape[1]/2, frame.shape[0]/2     # center coordinates of the frame
        
        barcodes = pyzbar.decode(frame)     # decoding of the image
        
        '''working with qr-code in the image'''
        if len(barcodes) > 0:   # check if the image includes qr-code
            
            for barcode in barcodes:

                (x, y, w, h) = barcode.rect     # coordinates and size of the qr-code
                x0 = (-xc + x + w/2)*100/k     # x coordinate
                #y0 = (yc - y - h/2)*100/k      # y coordinate 
                z0 = FOCAL_LENGTH*REAL_HIGTH*100/h      # z coordinate
            
                #distance = np.sqrt((x0/k)**2 + (y0/k)**2 + z0**2)    #distance between the camera and the object in meters  
                distance = np.sqrt((x0/k)**2 + z0**2)   # 2d distance
                angle = np.arctan(x0/z0)    # angle between the center axis and qr-code

                position.data = [distance, angle]   # final package for publishing 

        elif len(barcodes) == 0:    # if no qr-code, will publish constant value

            position.data = [-1]

        pub.publish(position)   # publishing the position to the topic /leader_position  



if __name__ =='__main__':
    try:
        scan()
    except rospy.ROSInterruptException:
        pass
