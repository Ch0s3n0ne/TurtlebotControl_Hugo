#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time 
import sys
from std_srvs.srv import Empty
from std_msgs.msg import String
from turtlesim.srv import *

x=0
y=0 
yaw=0

#vai tratar da informaçao referente à posiçao da tartaruga, cujo este programa subscreve
def poseCallback(pose_messsage):
	global x
	global y, yaw
	x=pose_messsage.x
	y=pose_messsage.y
	yaw=pose_messsage.theta

def spawner(x, y, theta, name):
    rospy.wait_for_service('/spawn')
    try:
        placing = rospy.ServiceProxy('/spawn', Spawn)
        resp1 = placing(x, y, theta , name)
        return resp1.name
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


def move(speed, distance, is_forward, turtleid ):

	velocity_message = Twist()

	if(turtleid==1):
		position_topic = "/turtle1/pose"
		cmd_vel_topic='turtle1/cmd_vel'
	else:
		position_topic = "/turtle2/pose"
		cmd_vel_topic='turtle2/cmd_vel'

	print position_topic
	pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)

	global x, y
	x0=x
	y0=y
	
	print ('x %f +++++ y %f  ' %(x,y))

	if(is_forward):
		velocity_message.linear.x=abs(speed)
	else:
		velocity_message.linear.x=-abs(speed)

	distance_moved = 0.0
	rate = rospy.Rate(10)

	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

	while True:
		rospy.loginfo("Turtlesim moves forwards")
		velocity_publisher.publish(velocity_message)

		rate.sleep()
		#rospy.Duration(1.0)

		distance_moved= distance_moved+ abs(0.5 * math.sqrt(((x-x0)**2) + ((y-y0)**2)))
		print distance_moved
		if not (distance_moved<distance):
			rospy.loginfo("reached")
			break

	#parar o robo quando a distancia é atingida 
	velocity_message.linear.x=0
	velocity_publisher.publish(velocity_message)

def go_to_goal(x_goal, y_goal, turtleid):

	global x, y, yaw
	velocity_message = Twist()


	if(turtleid==1):
		position_topic = "/turtle1/pose"
		cmd_vel_topic='turtle1/cmd_vel'
	else:
		position_topic = "/turtle2/pose"
		cmd_vel_topic='turtle2/cmd_vel'


	pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)

	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist ,queue_size=10)

	#print yaw
	#time.sleep(7)

	while(True):

		K_linear=1
		distance= abs(math.sqrt(((x_goal-x)**2)+((y_goal-y)**2)))
		linear_speed=distance * K_linear

		K_angular = 10.0
		desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
		angular_speed = (desired_angle_goal-yaw)*K_angular

		velocity_message.linear.x = linear_speed
		velocity_message.angular.z = angular_speed

		velocity_publisher.publish(velocity_message)
		print 'x= ', x , 'y=', y
		#print desired_angle_goal
		#break

		if (distance < 0.05):
			print "chegou"
			break


	


if __name__ == '__main__':
	try:


		rospy.init_node('basic_control', anonymous=True)

		x1=3 
		y1=4
		theta1=0
		name1=rospy.get_param("/controller_2/spawn_turtle_name")

		spawner(x1, y1, theta1, name1)



		
		vec_linear1=rospy.get_param("/controller_1/linear_speed")
		vec_linear2=rospy.get_param("/controller_2/linear_speed")
		#vec_angular=rospy.get_param("/controller_1/angular_speed")
		#move(vec_linear1,10, True, 1 )
		#move(vec_linear2,2, True,2  )

		#elipse(4,3)
		go_to_goal(1.0,1.0,1)
		move(vec_linear2,10, True,2)
		#circle()

	except rospy.ROSInterruptException:
		rospy.loginfo("node terminated.")
