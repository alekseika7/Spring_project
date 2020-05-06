#!/usr/bin/python

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2
from pyzbar import pyzbar

bridge = CvBridge()
twist = Twist()

rospy.init_node('code_scan_node')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)


def scan(data):
    
    try:
        cv_img = bridge.imgmsg_to_cv2(data, 'bgr8')
        barcodes = pyzbar.decode(cv_img)
        
        for barcode in barcodes:
            
            b_data = barcode.data.decode("utf-8")
            
            if len(b_data) > 0:
                rospy.loginfo(str(b_data))
                
                if b_data == 'front':
                    twist.linear.x = 1.0
                    twist.linear.y = 0.0
                    twist.linear.z = 0.0
                    twist.angular.x = 0.0
                    twist.angular.y = 0.0
                    twist.angular.z = 0.0
                elif b_data == 'back':
                    twist.linear.x = -1.0
                    twist.linear.y = 0.0
                    twist.linear.z = 0.0
                    twist.angular.x = 0.0
                    twist.angular.y = 0.0
                    twist.angular.z = 0.0
                elif b_data == 'right':
                    twist.linear.x = 0.0
                    twist.linear.y = 0.0
                    twist.linear.z = 0.0
                    twist.angular.x = 0.0
                    twist.angular.y = 0.0
                    twist.angular.z = 1.0
                elif b_data == 'left':
                    twist.linear.x = 0.0
                    twist.linear.y = 0.0
                    twist.linear.z = 0.0
                    twist.angular.x = 0.0
                    twist.angular.y = 0.0
                    twist.angular.z = -1.0
                else:
                    twist.linear.x = 0.0
                    twist.linear.y = 0.0
                    twist.linear.z = 0.0
                    twist.angular.x = 0.0
                    twist.angular.y = 0.0
                    twist.angular.z = 0.0
                    
            else:
                rospy.loginfo('No data')
                
            if b_data in ('front', 'back', 'left', 'right', 'stop'):
                pub.publish(twist)
            
    except CvBridgeError as e:
        rospy.loginfo(str(e))


if __name__ =='__main__':
    try:
        rospy.Subscriber('/cv_camera/image_raw', Image, scan)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    

