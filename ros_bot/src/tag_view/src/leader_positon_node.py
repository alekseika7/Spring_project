#!/usr/bin/python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
#from std_msgs.msg import Float32MultiArray, Float32
from geometry_msgs.msg import Twist
import cv2
from pyzbar import pyzbar
import numpy as np

bridge = CvBridge()

rospy.init_node('get_leader_node')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)

twist = Twist()

twist.linear.x = 0
twist.linear.y = 0
twist.linear.z = 0
twist.angular.x = 0
twist.angular.y = 0
twist.angular.z = 0


REAL_WIDTH = 0.05 #real lenght of the qr-code in meters
REAL_HIGTH = 0.05 #real heigth of the qr-code in meters

#focal length was calculated using real object size (5x5 cm), distance = 10cm
#and height of the object in pixels (aprox. 200 pixels)
FOCAL_LENGTH = 400 
k = 4000 #index for converting from pixels to meters

WORK_DISTANCE = 10  

def get_position(data):
    
    try:
        frame = bridge.imgmsg_to_cv2(data, 'bgr8')
        frame = cv2.resize(frame, (375, 500))
        xc, yc = frame.shape[1]/2, frame.shape[0]/2 #center coordinates of the frame
        
        barcodes = pyzbar.decode(frame)
        if len(barcodes) > 0:
            for barcode in barcodes:
                #coordinates and size of the qr-code
                (x, y, w, h) = barcode.rect
                #get coordinates of the qr-code in center axis in cm
                x0 = (-xc + x + w/2)*100/k     
                y0 = (yc - y - h/2)*100/k   
                z0 = FOCAL_LENGTH*REAL_HIGTH*100/h
            
                distance = np.sqrt((x0/k)**2 + (y0/k)**2 + z0**2)    #distance between the camera and the object in meters            
            
                #position = Float32MultiArray()
                #position.data = [distance, x0]

                if distance < WORK_DISTANCE:
                    twist.linear.x = -1
                elif distance > WORK_DISTANCE:
                    twist.linear.x = 1

                pub.publish(twist)

        elif len(barcodes) == 0:
            twist.linear.x = 0
            pub.publish(twist)
            
    except CvBridgeError as e:
        rospy.loginfo(str(e))



if __name__ =='__main__':
    try:
        rospy.loginfo("Ready to scan")
        rospy.Subscriber('/cv_camera/image_raw', Image, get_position)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
