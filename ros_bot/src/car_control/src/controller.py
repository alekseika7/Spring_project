#!/usr/bin/python3.7

import rospy
from std_msgs.msg import Float32MultiArray, Float32

import numpy as np

rospy.init_node('controller_node')
pub = rospy.Publisher('/controller_output', Float32, queue_size = 1)
rate = rospy.Rate(10)

REF_DISTANCE = 10
Kpl = 0.1
Kpa = 0.1
MIN_V = 0.4
MAX_V = 0.5


def controller(position):

    if len(position.data) == 1:
        linear = 0
    else:
        distance = position.data[0]
        angle = position.data[1]
        err_l = distance - REF_DISTANCE
        err_a = angle
    
        linear = Kpl*err_l
        if np.abs(linear) > MAX_V:
            linear = np.sign(linear)*MAX_V
        elif np.abs(linear) < MIN_V:
            linear = np.sign(linear)*MIN_V

    pub.publish(linear)
    rospy.loginfo(str(linear)) 
    rate.sleep()

if __name__ == '__main__':
    try:
        rospy.loginfo("Controller is running")
        rospy.Subscriber('/leader_position', Float32MultiArray, controller)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
