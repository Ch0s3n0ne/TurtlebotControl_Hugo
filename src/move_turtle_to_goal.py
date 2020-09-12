#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
from turtlebot_control.srv import TurtleGoal,TurtleGoalResponse


def handle_goal(req):

	 print("Giding the bot to x= %s and y= %s " %(req.goal_x, req.goal_y))

	 Response=True

	 if (req.goal_x<0.0 or req.goal_y<0.0):
		Response=False
	 elif (req.goal_x>10.0 or req.goal_y>10.0):
		Response=False

   	 return TurtleGoalResponse(Response)
    

def goal_server():
    rospy.init_node('move_turtle_to_goal')
    s = rospy.Service('move_turtle_to_goal', TurtleGoal, handle_goal)
    print("Give the coordenates for the ending position")
    rospy.spin()

if __name__ == "__main__":
   goal_server()