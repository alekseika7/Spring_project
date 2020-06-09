#!/usr/bin/python3.7
import rospy
from std_msgs.msg import Float32

import numpy as np

#from gui_for_test import car
import car
car.init()

def go(data):
    speed = round(data.data, 2)
    if speed > 0:
        #car.turn('right', 0.35)
    #elif data.angular.z < 0:
        #car.turn('left', 0.35)
    #elif data.linear.x > 0:
        car.move('front', speed)
    elif speed < 0:
        car.move('back', np.abs(speed))
    else:
        car.motors_off()
        
    rospy.loginfo('speed = ' + str(speed))   
        
        
def listen():
    
    rospy.init_node('object', anonymous=True)
    rospy.Subscriber('/controller_output', Float32, go)
    
    rospy.loginfo('bot is ready to move')
    
    rospy.spin()
    

if __name__ =='__main__':
    try:
        listen()
        car.off_n_reset()
    except rospy.ROSInterruptException:
        pass
