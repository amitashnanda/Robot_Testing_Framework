#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool
import os, sys
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
import time
from osrf_gear.srv import VacuumGripperControl
import json 

class RobotArmGripper:

    def __init__(self,flag):
        self.flag = flag
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
            if flag == False:
                pub = rospy.Publisher('/ariac/arm1/backToInitialCommand',String, queue_size=10)
                pub.publish('True')
                self.flag = True
        except rospy.ServiceException as exc:
            self.grip(flag)

    def armLocation(self,data):
        jt0 = data.position[0]
        jt1 = data.position[1]
        jt2 = data.position[2]
        jt3 = data.position[3]
        jt4 = data.position[4]
        jt5 = data.position[5]
        jt6 = data.position[6]

        # -0.35, 3.14,  -0.5,  2.3, 3.05, -1.59, 0.126
        # 1.18, 1.507,  0.38,  -0.38, 1.55, 1.75, 0.127
        approx_state_1 = (-0.35 - jt1)**2 + (3.14 - jt3)**2 + (-0.5 - jt2)**2 +  (2.3-jt0)**2 + (3.05-jt4)**2 + (-1.59-jt5)**2 + (0.126-jt6)**2
        approx_state_2 =  (1.18 - jt1)**2 + (1.507 - jt3)**2 + (0.38 - jt2)**2 + (-0.38 -jt0)**2 + (1.55-jt4)**2 + (1.75-jt5)**2 + (0.127-jt6)**2
        # print (approx_state_1,'-',approx_state_2)
        if approx_state_1 <= 0.005:
            self.grip(True)
            # self.status_json['Testcase_2'] = True
            # pub_status_test_case_0 = rospy.Publisher('/ariac/arm1/testcase/status',String,queue_size=10)
            # pub_status_test_case_0.publish(json.dumps(self.status_json))
        if approx_state_2 <= 0.005:
            self.grip(False)          
            # self.status_json['Testcase_4'] = True
            # pub_status_test_case_0 = rospy.Publisher('/ariac/arm1/testcase/status',String,queue_size=10)
            # pub_status_test_case_0.publish(json.dumps(self.status_json))

    def arm_location_call(self): 
        while not rospy.is_shutdown() and self.flag == False:
            sub = rospy.Subscriber('/ariac/arm1/joint_states', JointState, self.armLocation)
            rospy.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node("arm_state_1", log_level=rospy.DEBUG)
        rate = rospy.Rate(1)
    except:
        pass
    initRoboArm = RobotArmGripper(False)
    initRoboArm.arm_location_call()