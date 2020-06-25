#!/usr/bin/python3.7

import rospy
import time
from std_msgs.msg import Int16MultiArray
from simple_pid import PID

rospy.init_node('controller_node')
pub = rospy.Publisher('/controller_output', Int16MultiArray, queue_size = 1)

position = Int16MultiArray()  # array for the distance and angle
control = Int16MultiArray()  # array for control

SETPOINT = 230

def controller(position):
    if len(position.data) == 1:
        #linear = 0
        control.data = [999, 0]
        print("No QR-code")

    else:

        distance = position.data[0]
        angle = position.data[1]

        pid_linear = PID(-0.5, -1, -0.05, setpoint=distance)
        pid_linear.output_limits = (-15, 45)

        pid_angular = PID(1.5, 2, 0.01, setpoint=angle)
        pid_angular.output_limits = (-25, 25)

        pid_linear.setpoint = SETPOINT   #distance in mm
        pid_angular.setpoint = 0   # zero angle needed

        #if current_time - start_time > 0.5:
        #start_time = time.time()
        #last_time = start_time

        pid_linear.sample_time = 0.01  # update every 0.001 seconds
        pid_angular.sample_time = 0.01  # update every 0.001 seconds

        linear = pid_linear(distance)
        
        if linear > 0:
            linear += 15
        elif linear < 0:
            linear -= 15
        
        angular = pid_angular(angle)

        if angular > 0:
            angular += 5
        elif angular < 0:
            angular -= 5
            
        control.data = [int(linear), int(angular)]   # final package for publishing
        print(int(linear), int(angular))

    pub.publish(control)
    #rospy.loginfo(str(linear))

if __name__ == '__main__':
    try:
        rospy.loginfo("Controller is running")
        rospy.Subscriber('/leader_position', Int16MultiArray, controller)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
