#!/usr/bin/python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32MultiArray
import cv2
from pyzbar import pyzbar
import numpy as np

bridge = CvBridge()

rospy.init_node('get_leader_node')
pub = rospy.Publisher('/leader_position', Float32MultiArray, queue_size = 1)

REAL_WIDTH = 0.05 #real lenght of the qr-code in meters
REAL_HIGTH = 0.05 #real heigth of the qr-code in meters

#focal length was calculated using real object size (5x5 cm), distance = 10cm
#and height of the object in pixels (aprox. 200 pixels)
FOCAL_LENGTH = 400 
k = 4000 #index for converting from pixels to meters

def get_position(data):
    
    try:
        frame = bridge.imgmsg_to_cv2(data, 'bgr8')
        frame = cv2.resize(frame, (375, 500))
        xc, yc = int(frame.shape[1]/2), int(frame.shape[0]/2) #center coordinates of the frame
        
        barcodes = pyzbar.decode(frame)
        
        for barcode in barcodes:
            #coordinates and size of the qr-code
            (x, y, w, h) = barcode.rect
            
            #get coordinates of the qr-code in center axis in cm
            x0 = round((-xc + x + w/2)*100/k, 3)     
            y0 = round((yc - y - h/2)*100/k, 3)   
            z0 = round(FOCAL_LENGTH*REAL_HIGTH*100/h, 3)
            
            distance = round(np.sqrt((x0/k)**2 + (y0/k)**2 + z0**2), 3)    #distance between the camera and the object in meters            
            
            position = Float32MultiArray()
            
            position.data = [distance, x0]
            
            pub.publish(position)
            
            
    except CvBridgeError as e:
        rospy.loginfo(str(e))



if __name__ =='__main__':
    try:
        rospy.Subscriber('/cv_camera/image_raw', Image, get_position)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass