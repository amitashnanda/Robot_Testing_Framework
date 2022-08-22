def talker():
        pub1 = rospy.Publisher('armstate' , bool , queue_size=10)
        rospy.init_node('talker', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            hello_str = "hello world %s" % rospy.get_time()
            rospy.loginfo(hello_str)
            pub1.publish(hello_str)
            rate.sleep()