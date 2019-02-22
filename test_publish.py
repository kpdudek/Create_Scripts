#!/usr/bin/env python

import rospy
import numpy as np
from nav_msgs.msg import Odometry
from ca_msgs.msg import Bumper, ChargingState
from sensor_msgs.msg import JointState, Joy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist, PoseStamped, Pose
import std_msgs.msg
import geometry_msgs.msg
import tf
import os
import sys
import time
hostname = os.uname()[1]


class CreateWayPoint(object):
    def __init__(self):
        rospy.init_node("waypoint_read")
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(25)

        self.cmd_vel = Twist()
        self.cmd_vel.linear.x = .05
        self.cmd_vel.angular.z = .1

    def start_waypoint(self):
        while not rospy.is_shutdown():
            self.cmd_vel_pub.publish(self.cmd_vel)
            self.rate.sleep()

if __name__== "__main__":
	create_waypoint = CreateWayPoint()
	create_waypoint.start_waypoint()
