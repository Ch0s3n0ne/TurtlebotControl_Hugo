#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
#esta informaçao das mensagens pode se tirar do terminal
from turtlebot_control.srv import turtle_spawn,turtle_spawnResponse

Response="turtle_x"

def handle_goal(req):

	 print("Placing the bot at x= %s, y= %s, theta= %s with the name %s   " %(req.x, req.y, req.theta ,req.name))

	 Response=req.name 

   	 return turtle_spawnResponse(Response)
    

def goal_server():
    rospy.init_node('Spawn')
    s = rospy.Service('Spawn', turtle_spawn, handle_goal)
    print("Give the coordenates for the placing")
    rospy.spin()

if __name__ == "__main__":
   goal_server()

