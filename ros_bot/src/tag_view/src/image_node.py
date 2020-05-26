#!/usr/bin/python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

rospy.init_node('image_node')
bridge = CvBridge()


def callback(data):
    try:
        frame = bridge.imgmsg_to_cv2(data, "bgr8")
        frame = cv2.resize(frame,(500, 375))
        cv2.imshow('Scanner', frame)
        cv2.waitKey(1) & 0xFF
        
    except CvBridgeError as e:
        rospy.loginfo(str(e))


if __name__ =='__main__':
    try:
        rospy.Subscriber('/cv_camera/image_raw', Image, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass