#!/usr/bin/env python

from gazebo_msgs.srv import GetModelState
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState 
from gazebo_msgs.srv import GetWorldProperties, GetModelProperties
import rospy
from gazebo_msgs.srv import GetLinkProperties ,GetLinkState

class GazeboModels:

    def getAllModels(self):
        success = True
        get_world_properties = rospy.ServiceProxy('/gazebo/get_world_properties', GetWorldProperties)
        object_list = list()
        try:
            resp1 = get_world_properties()
        except rospy.ServiceException:
            print("error")
            success = False
        if success:
            get_model_properties = rospy.ServiceProxy('/gazebo/get_model_properties', GetModelProperties)
            for model in resp1.model_names:
                try:
                    model_properties = get_model_properties(model)
                except rospy.ServiceException:
                    success = False
                if success:
                    for body in model_properties.body_names:
                        object_list.append(model + '::' + body)
        # print(object_list)
        # print(type(object_list))

        return object_list
        

class Block:
    def __init__(self, name, relative_entity_name):
        self._name = name
        self._relative_entity_name = relative_entity_name

class GetModelLocation:

    def __init__(self,modelName):
        self._blockListDict = {
            'block_a': Block(modelName, 'link')
        }
        self.initialModelLocation = None
        self.initialModelMass = None
        self.initialLinkLocation = None

    def showGazeboModels(self):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            for block in self._blockListDict.values():
                blockName = str(block._name)
                resp_coordinates = model_coordinates(blockName, block._relative_entity_name)
                self.initialModelLocation = resp_coordinates
        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
        # print self.initialModelLocation
        return self.initialModelLocation

    def showObjectMass(self):
        try:
            model_mass = rospy.ServiceProxy('/gazebo/get_link_properties', GetLinkProperties)
            for block in self._blockListDict.values():
                blockName = str(block._name)
                resp_mass = model_mass(blockName)
                self.initialModelMass = resp_mass

 

        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
        # print self.initialModelLocation
        return self.initialModelMass

    # def showLinkState(self):
    #     try:
    #         model_coordinates_1 = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
    #         for block in self._blockListDict.values():
    #             blockName1 = str(block._name)
    #             resp_coordinates_1 = model_coordinates_1(blockName1, block._relative_entity_name)
    #             self.initialLinkLocation = resp_coordinates_1
    #     except rospy.ServiceException as e:
    #         rospy.loginfo("Get Link State service call failed:  {0}".format(e))
    #     # print self.initialModelLocation
    #     return self.initialLinkLocation


class SetModelLocation:

    def setGazeboModel(self,modelName,X,Y,Z):
        rospy.wait_for_service('/gazebo/set_model_state')
        try:
            state_msg = ModelState()
            state_msg.model_name = modelName
            state_msg.pose.position.x = X
            state_msg.pose.position.y = Y
            state_msg.pose.position.z = Z
            state_msg.pose.orientation.x = 0
            state_msg.pose.orientation.y = 0
            state_msg.pose.orientation.z = 0
            state_msg.pose.orientation.w = 0
            print(X,Y,Z,modelName)
            try:
                set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
                resp = set_state( state_msg )

            except rospy.ServiceException as e:
                print("Service call failed: %s" % e)
        except rospy.ServiceException as e:
            rospy.loginfo("Set Model State service call failed:  {0}".format(e))


# if __name__ == '__main__':
#     getModelLoc = GetModelLocation('bin4|gasket_part_5')
#     getModelLoc.showGazeboModels()

#     setModelLoc = SetModelLocation()
#     setModelLoc.setGazeboModel()