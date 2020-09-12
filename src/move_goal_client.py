#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
#esta informaçao das mensagens pode se tirar do terminal
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time 
import sys
from std_srvs.srv import Empty
from std_msgs.msg import String
from turtlebot_control.srv import *

x1=0;
y1=0;
yaw=0;

def Autorization(x, y):
    rospy.wait_for_service('move_turtle_to_goal')
    try:
        position = rospy.ServiceProxy('move_turtle_to_goal', TurtleGoal)
        resp1 = position(x, y)
        return resp1.success
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y]"%sys.argv[0]


#vai tratar da informaçao referente à posiçao da tartaruga, cujo este programa subscreve
def poseCallback(pose_messsage):
	global x1
	global y1, yaw
	x1=pose_messsage.x
	y1=pose_messsage.y
	yaw=pose_messsage.theta


def go_to_goal(x_goal, y_goal):

	global x1, y1, yaw
	velocity_message = Twist()

	rospy.init_node('basic_control', anonymous=True)

	cmd_vel_topic='turtle1/cmd_vel'
	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist ,queue_size=10)

	position_topic = "/turtle1/pose"
	pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)


	#print yaw
	#time.sleep(7)

	while(True):

		K_linear=1
		distance= abs(math.sqrt(((x_goal-x1)**2)+((y_goal-y1)**2)))
		linear_speed=distance * K_linear

		K_angular = 3.0
		desired_angle_goal = math.atan2(y_goal-y1, x_goal-x1)
		angular_speed = (desired_angle_goal-yaw)*K_angular

		velocity_message.linear.x = linear_speed
		velocity_message.angular.z = angular_speed

		velocity_publisher.publish(velocity_message)
		print 'x= ', x1 , 'y=', y1
		#print desired_angle_goal
		#break

		if (distance < 0.05):
			print "It arrived"
			break

			

if __name__ == "__main__":


    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
    	#print("sss")
        #print(usage())
        sys.exit(1)
    print("Requesting x = %s and y= %s"%(x, y))

    print("x = %s and y= %s is a %s location "%(x, y, Autorization(x, y)))

    if(Autorization(x,y)==True):
    	print "Pode avançar"
    	go_to_goal(x,y)
    else:
    	print "Please insert a valid location"

