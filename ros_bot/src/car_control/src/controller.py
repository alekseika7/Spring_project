#!/usr/bin/python3.7

import rospy
import time
from std_msgs.msg import Int16MultiArray
from simple_pid import PID

rospy.init_node('controller_node')
pub = rospy.Publisher('/controller_output', Int16MultiArray, queue_size = 1)

position = Int16MultiArray()  # array for the distance and angle
control = Int16MultiArray()  # array for control

SETPOINT = 150

def controller(position):
    if len(position.data) == 1:
        linear = 0
        control.data = [0, 0]
        #print("Can't see QR-code")

    else:

        distance = position.data[0]
        angle = position.data[1]

        pid_linear = PID(-1.0, -0.5, -0.12, setpoint=distance)
        pid_linear.output_limits = (-50, 50)

        pid_angular = PID(1, 1.5, 0.12, setpoint=angle)
        pid_angular.output_limits = (-40, 40)

        pid_linear.setpoint = SETPOINT   #distance in mm
        pid_angular.setpoint = 0   # zero angle needed

        #if current_time - start_time > 0.5:
        #start_time = time.time()
        #last_time = start_time

        pid_linear.sample_time = 0.001  # update every 0.001 seconds
        pid_angular.sample_time = 0.001  # update every 0.001 seconds

        linear = pid_linear(distance)
        angular = pid_angular(angle)

        control.data = [int(linear), int(angular)]   # final package for publishing
        #print(int(linear), int(angular))

    pub.publish(control)
    #rospy.loginfo(str(linear))

if __name__ == '__main__':
    try:
        rospy.loginfo("Controller is running")
        rospy.Subscriber('/leader_position', Int16MultiArray, controller)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass