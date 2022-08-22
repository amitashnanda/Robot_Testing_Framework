#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool
import os
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
import time
from osrf_gear.srv import VacuumGripperControl
import json

class RobotArmController:

    def __init__(self):
        pass
        # self.status_json = {
        #     'Testcase_0': False,
        #     'Testcase_1': False,
        #     'Testcase_2': False,
        #     'Testcase_3': False,
        #     'Testcase_4': False
        # }

    def grip(self,flag):
        try:
            gripper_control = rospy.ServiceProxy('/ariac/arm1/gripper/control', VacuumGripperControl)
            response = gripper_control(flag)
        except rospy.ServiceException as exc:
            rospy.logerr("Failed to control the gripper: %s" % exc) 

    def arm_controller(self, positions): 
        while rospy.get_rostime().to_sec() == 0.0:
            time.sleep(0.1)
            # print rospy.get_rostime().to_sec()
        self.grip(False)
        rospy.sleep(1)
        pub = rospy.Publisher('/ariac/arm1/arm/command', JointTrajectory, queue_size=10)
        msg = JointTrajectory()
        msg.header.stamp = rospy.Time.now()
        msg.joint_names = [
            'linear_arm_actuator_joint', 
            'shoulder_pan_joint', 
            'shoulder_lift_joint', 
            'elbow_joint', 
            'wrist_1_joint', 
            'wrist_2_joint', 
            'wrist_3_joint'
            ]
       
        points_dict = dict()
        count=0
        for eachPose in positions:
            key = 'point_' + str(count)
            points_dict[key] = JointTrajectoryPoint()
            points_dict[key].positions = eachPose[0]
            points_dict[key].time_from_start = rospy.Duration(float(eachPose[1]))
            count += 1 

            
        msg.points = points_dict.values()
        rospy.loginfo("Sending commands:\n" + str(msg))
        # self.status_json['Testcase_1'] = True
        # pub_status_test_case_0 = rospy.Publisher('/ariac/arm1/testcase/status',String,queue_size=10)
        # pub_status_test_case_0.publish(json.dumps(self.status_json))
        while not rospy.is_shutdown():
            pub.publish(msg)
            rospy.sleep(1)
            
   

    def movearm2Gear(self):
        pub_init = rospy.Publisher('/ariac/arm1/backToInitialCommand',String, queue_size=10)
        pub_init.publish('False')
        # self.status_json['Testcase_0'] = True
        # pub_status_test_case_0 = rospy.Publisher('/ariac/arm1/testcase/status',String,queue_size=10)
        # pub_status_test_case_0.publish(json.dumps(self.status_json))
        p0 = [0.15, 3.14,  -1.570,  2.14, 3.1, -1.59, 0.126]
        t0 = 2
        p1 = [-0.35, 3.14,  -0.6,  2.3, 3.0, -1.59, 0.126]
        t1 = 4
        p2 = [-0.35, 3.14,  -0.5,  2.3, 3.05, -1.59, 0.126]
        t2 = 6
    
        self.arm_controller([[p0,t0],[p1,t1],[p2,t2]])
        

if __name__ == '__main__':
    try:
        rospy.init_node("pick_gear_controller_node", log_level=rospy.DEBUG)
        rate = rospy.Rate(1)
    except:
        pass
    initRoboArm = RobotArmController()
    initRoboArm.movearm2Gear()
