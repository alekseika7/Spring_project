#!/usr/bin/python3.7
import rospy
from geometry_msgs.msg import Twist
#from gui_for_test import car
import car
car.init()

def go(data):
    
    if data.angular.z > 0:
        car.turn('right', 0.35)
    elif data.angular.z < 0:
        car.turn('left', 0.35)
    elif data.linear.x > 0:
        car.move('front', 0.35)
    elif data.linear.x < 0:
        car.move('back', 0.35)
    else:
        car.motors_off()
        
    rospy.loginfo('Linear = %f ; Angular = %f', data.linear.x, data.angular.z)   
        
        
def listen():
    
    rospy.init_node('object', anonymous=True)
    rospy.Subscriber('/cmd_vel', Twist, go)
    
    rospy.loginfo('bot is ready to move')
    
    rospy.spin()
    

if __name__ =='__main__':
    try:
        listen()
        car.off_n_reset()
    except rospy.ROSInterruptException:
        pass
