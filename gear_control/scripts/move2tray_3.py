#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import os
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
import time
from osrf_gear.srv import VacuumGripperControl
from osrf_gear.msg import VacuumGripperState
import json

class MoveToTray3:

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
                # self.status_json['Testcase_3'] = True
                # pub_status_test_case_3 = rospy.Publisher('/ariac/arm1/testcase/status',String,queue_size=10)
                # pub_status_test_case_3.publish(json.dumps(self.status_json))
                # while not rospy.is_shutdown():
                #     pub.publish(msg)
                #     rospy.sleep(1)
        while not rospy.is_shutdown():
            pub.publish(msg)
            rospy.sleep(1)
                
            




    def movearm2Gear(self,data):
        rospy.sleep(11)
        # p0 = [0.0, 3.14,  -1.570,  2.14, 3.27, -1.51, 0.0]
        # t0 = 2
        # p1 = [1.0, 1.85,  0,  -0.38, 1.57, -1.51, 0.00]
        # t1 = 5
        p2 = [1.0, 1.507,  0,  -0.38, 0.38, -1.51, 0.00]
        t2 = 7
        # p3 = [1.18, 1.507,  0.38,  -0.38, 1.55, 1.75, 0.127]
        # t3 = 10
        #print(len(data.points))
        # if (len(data.points) == 3):
        if data.points[0].positions[0] == 1.0 and data.points[0].positions[1] == 1.85 and data.points[0].positions[2] == 0 and data.points[0].positions[3] == -0.38 and data.points[0].positions[4] == 1.57 and data.points[0].positions[5] == -1.51 and data.points[0].positions[6] == 0.00:
            self.arm_controller([[p2,t2]])
        
        
    def listenGripperState3(self):
        while not rospy.is_shutdown():
            sub = rospy.Subscriber('/ariac/arm1/arm/command',JointTrajectory ,self.movearm2Gear)
            rospy.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node("put_gear_on_tray_3", log_level=rospy.DEBUG)
        rate = rospy.Rate(1)
    except:
        pass
    initRoboArm = MoveToTray3()
    initRoboArm.listenGripperState3()
