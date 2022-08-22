#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool
import os
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
import time
from osrf_gear.srv import VacuumGripperControl
from osrf_gear.msg import VacuumGripperState

class BackToZero:

    def __init__(self):
        pass

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
        count=1
        for eachPose in positions:
            key = 'point_' + str(count)
            points_dict[key] = JointTrajectoryPoint()
            points_dict[key].positions = eachPose[0]
            points_dict[key].time_from_start = rospy.Duration(float(eachPose[1]))
            count += 1 

            
        msg.points = points_dict.values()
        rospy.loginfo("Sending commands:\n" + str(msg))
      
        while not rospy.is_shutdown():
            pub.publish(msg)
            rospy.sleep(1)
            
   

    def backToInitial(self,data):
       
        p0 = [0.0, 3.14,  -1.570,  2.14, 3.27, -1.51, 0.0]
        t0 = 2
        # print(data.data, type(data.data))
        if (data.data == 'True'):
            print 'inside'
            self.arm_controller([[p0,t0]])

    def inititalStateFlag(self):
        while not rospy.is_shutdown():
            sub = rospy.Subscriber('/ariac/arm1/backToInitialCommand',String,self.backToInitial)
            rospy.sleep(1)
#     def b2zero(self):
#         os.system('''rostopic pub /ariac/arm1/arm/command trajectory_msgs/JointTrajectory    "{joint_names: \
#         ['linear_arm_actuator_joint',  'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'], \
#      points: [ \
# {time_from_start: {secs: 5}, \
#         positions: [0.0, 3.14,  -1.570,  2.14, 3.27, -1.51, 0.0]}, \
# ]}" -1''')

if __name__ == '__main__':
    try:
        rospy.init_node("back_initial_position", log_level=rospy.DEBUG)
        rate = rospy.Rate(1)
    except:
        pass
    initRoboArm = BackToZero()
    initRoboArm.inititalStateFlag()
    # initRoboArm.b2zero()
