#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
#esta informaçao das mensagens pode se tirar do terminal
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time 
from turtlesim.srv import Spawn
from std_srvs.srv import Empty
from std_msgs.msg import String


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


def move(speed, distance, is_forward):

	velocity_message = Twist()

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

	cmd_vel_topic = 'cmd_vel'
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

#def rotate (angular_speed_degree, relative_angle_degree, clockwise):
#def elipse(a,b,clockwise):
def go_to_goal(x_goal, y_goal):
	global x, y, yaw
	velocity_message = Twist()

	cmd_vel_topic='/turtle1/cmd_vel'

	#print yaw
	#time.sleep(7)

	while(True):

		K_linear=1
		distance= abs(math.sqrt(((x_goal-x)**2)+((y_goal-y)**2)))
		linear_speed=distance * K_linear

		K_angular = 3.0
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

def print_screen():

	print "A reiniciar o sistema"



def circle():

	velocity_message=Twist()
	rate = rospy.Rate(10)
	i=0

	while(i<100):

		velocity_message.linear.x=rospy.get_param("/controller_1/linear_speed")

		velocity_message.angular.z=rospy.get_param("/controller_1/angular_speed")

		cmd_vel_topic = 'cmd_vel'
		velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)


		velocity_publisher.publish(velocity_message)
		print i
		i=i+1
		rate.sleep()


	the_service="/reset"
	s = rospy.Service(the_service, Empty, print_screen)
	rospy.spin()
	#rospy.wait_for_message(the_service, Empty, timeout=None)



def elipse(a,b):
	velocity_message = Twist()

	global x, y

	x0=5.544444561
	y0=5.544444561

	#print ('x0 %f +++++ y0 %f  ' %(x0,y0))

	#x1=0

	x1=a
	while(x1>=0):		
		 y1=b*math.sqrt((1-(x1/a)**2))
		 xfinal=x1+x0
		 yfinal=y1+y0
		 print ('x1 %f xfinal %f ---- y1 %f yfinal %f  ' %(x1,xfinal,y1,yfinal))
		 go_to_goal(xfinal,yfinal)
		 x1=x1-0.05

	#print "acabou"
	#print ('x %f ---- y %f   ' %(x,y))
	#time.sleep(3)

	x0=x

	while(x1<=a):
		 y1=b*math.sqrt((1-(x1/a)**2))
		 xfinal=x0-x1
		 yfinal=y1+y0
		 print ('x1 %f xfinal %f ---- y1 %f yfinal %f  ' %(x1,xfinal,y1,yfinal))
		# time.sleep(6)
		 go_to_goal(xfinal,yfinal)
		 x1=x1+0.05
	
	x0=x


	while(x1>=0):
		 y1=(-b*math.sqrt((1-(x1/a)**2)))
		 xfinal=x1+x0
		 yfinal=y1+y0
		 print ('x1 %f xfinal %f ---- y1 %f yfinal %f  ' %(x1,xfinal,y1,yfinal))
		# time.sleep(6)
		 go_to_goal(xfinal,yfinal)
		 x1=x1-0.5


	x0=x

	while(x1<=a):
		 y1=(-b*math.sqrt((1-(x1/a)**2)))
		 xfinal=x1+x0
		 yfinal=y1+y0
		 print ('x1 %f xfinal %f ---- y1 %f yfinal %f  ' %(x1,xfinal,y1,yfinal))
		# time.sleep(6)
		 go_to_goal(xfinal,yfinal)
		 x1=x1-0.5





	print "acabou"	





	
	#velocity_message.linear.x=0
	#velocity_message.angular.z=0;
	#velocity_publisher.publish(velocity_message)



##def setDesieredOrientatiion(desired_angle_radians):




if __name__ == '__main__':
	try:

		rospy.init_node('basic_control', anonymous=True)

		cmd_vel_topic='cmd_vel'
		velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist ,queue_size=10)

		position_topic = "/turtle1/pose"
		pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)

		#the_service="/spawn"
		#s = rospy.Service(the_service, Empty, print_screen)

		#	setDesiredOrientation(math.radian(90))
		
		#vec_linear=rospy.get_param("/controller_1/linear_speed")
		#vec_angular=rospy.get_param("/controller_1/angular_speed")
		#move(vec_linear,10, True)
		#elipse(4,3)
		go_to_goal(1.0,1.0)
		#circle()

	except rospy.ROSInterruptException:
		rospy.loginfo("node terminated.")
