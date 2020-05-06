#!/usr/bin/python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

rospy.init_node('image_node')
bridge = CvBridge()


def callback(data):
    try:
        cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
        cv2.imshow('Scanner', cv_img)
        cv2.waitKey(1) & 0xFF
    except CvBridgeError as e:
        rospy.loginfo(str(e))


if __name__ =='__main__':
    try:
        rospy.Subscriber('/cv_camera/image_raw', Image, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass