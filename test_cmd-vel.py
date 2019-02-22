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
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.rate = rospy.Rate(25)

        self.cmd_vel = Twist()
        self.cmd_vel.linear.x = .05
        self.cmd_vel.angular.z = .1

        self.state = 2
        self.buttons = []
        self.axes = []

        self.last_state = 0

    def joy_callback(self,data):
        if data.buttons[1] == 1:
            rospy.signal_shutdown("stop")

        self.buttons = data.buttons
        self.axes = data.axes

        if self.buttons[3] == 1: #Y
            self.state = 0
        if self.buttons[0] == 1: #A
            self.state = 1
        if self.buttons[2]==1: #X
            self.state = 2

        vel = self.run_state()

        self.cmd_vel.linear.x = vel[0]
        self.cmd_vel.angular.z = vel[1]

        self.cmd_vel_pub.publish(self.cmd_vel)


    def idle(self):
        vel = [0.0,0.0]
        self.last_state = 0
        return vel

    def manual_control(self):
        self.last_state = 1
        vel = [0.0,0.0]
        return vel

    def auto_circles(self):
        vel = [self.cmd_vel.linear.x,self.cmd_vel.angular.z]

        if not self.last_state == self.state:
            vel[0] = .1
            vel[1] = .5

        if self.buttons[13]==1:
            vel[0] += .01
            #print(data.buttons[10])
        elif self.buttons[14]==1:
            vel[0] -= .01
            #print(data.buttons[11])

        if self.buttons[12]==1:
            vel[1] += .1
        elif self.buttons[11]==1:
            vel[1] -= .1

        self.last_state = 2

        return vel


    def run_state(self):
        if self.state == 0:
            if not self.last_state == self.state:
                print("Idle")
            vel = self.idle()

        if self.state == 1:
            if not self.last_state == self.state:
                print("Manual Control")
            vel = self.manual_control()

        elif self.state ==2:
            if not self.last_state == self.state:
                print("Auto Circles")
            vel = self.auto_circles()
        return vel

    def start_waypoint(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__== "__main__":
	create_waypoint = CreateWayPoint()
	create_waypoint.start_waypoint()
