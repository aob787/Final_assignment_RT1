#! /usr/bin/env python

#https://answers.ros.org/question/80646/python-sending-goals-to-the-navigation-stack/

import rospy

# import ros message
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf import transformations
# import ros service
from std_srvs.srv import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseFeedback, MoveBaseResult
import time
import actionlib

import math


# 0 - go to point
# 1 - wall following
client_ = None

def go_to_switch(req):
    global activate_
    activate_ = req.data
    client_.cancel()
    print ("Status of node goto-rt3 = "+ str(activate_))
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res


def main():
    time.sleep(2)
    global activate_, client_

    rospy.init_node('goto_pos_rt3')
    ##https://answers.ros.org/question/316592/problem-when-publishing-to-move_basegoal/
    #http://wiki.ros.org/navigation/Tutorials/SendingSimpleGoals
    client_ = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    rospy.loginfo("Waiting for move base server")
    client.wait_for_server()

    srv = rospy.Service('activate_goto', SetBool, go_to_switch)


    while not rospy.is_shutdown():

        if activate_ == False:
            continue
        else:
            activate_ = False
            goal = MoveBaseGoal()
            goal.target_pose.pose.position.x = rospy.get_param('des_pos_x')
            goal.target_pose.pose.position.y = rospy.get_param('des_pos_y')
            goal.target_pose.header.frame_id = 'map'
            goal.target_pose.pose.orientation.w  = 1
            print ("Goal X Y = " + str(move_base_goal.target_pose.pose.position.x) + ", " + str(move_base_goal.target_pose.pose.position.y))
            client_.send_goal(goal)
            result = client_.wait_for_result()
            print ("Status : " str(result))


if __name__ == "__main__":
    main()
