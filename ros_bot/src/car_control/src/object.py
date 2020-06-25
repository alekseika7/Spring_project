#!/usr/bin/python3.7

import rospy
import car
from std_msgs.msg import Int16MultiArray

car.init()

def go(data):
    if (data.data[0] > 100):
        car.motors_off()
    else:    
        linear_speed = data.data[0]/100
        rotation_speed = data.data[1]/100

        speed_l = linear_speed + rotation_speed
        speed_r = linear_speed - rotation_speed

        car.direct_controll(speed_l, speed_r)

    #print(speed_l, speed_r)

def listen():

    rospy.init_node('object', anonymous=True)
    rospy.Subscriber('/controller_output', Int16MultiArray, go)

    rospy.loginfo('bot is ready to move')

    rospy.spin()


if __name__ =='__main__':
    try:
        listen()
        car.off_n_reset()
    except rospy.ROSInterruptException:
        pass
