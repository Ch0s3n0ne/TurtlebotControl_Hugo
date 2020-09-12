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
from turtlesim.srv import *

def spawner(x, y, theta, name):
    rospy.wait_for_service('/spawn')
    try:
        add_two_ints = rospy.ServiceProxy('/spawn', Spawn)
        resp1 = add_two_ints(x, y, theta , name)
        return resp1.name
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 5:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        theta = int(sys.argv[3])
        name = sys.argv[4]
    else:
        print(usage())
        sys.exit(1)
    print("Requesting %s--%s--%s--%s"%(x, y, theta,name ))
    print("x= %s  y= %s theta= %s and with name %s ___ %s" %(x, y,theta , name ,spawner(x, y, theta, name)))