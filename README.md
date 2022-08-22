# Robot_Testing_Framework
> A state of the art Robot Testing Platform which innovatively tests the robots in a real world scenario in a cloud environment!


## Features 📋
⚡️ Chaos Location Perturbation\
⚡️ Chaos Node Kill\
⚡️ Chaos Add Objects\
⚡️ Chaos Latency

> AWS Robomaker is the amazon cloud service which enables the robotics development to be carried out on  the cloud. 
> Robomaker makes use of colcon to build packages and bundle them. Colcon works well with ROS2 and is  back compatible with ROS1. Colcon is just like catkin_make that we use to build project on ROS1.




## Installation & Deployment 📦
1. Clone the repository.
2. Download the universal_robot folder from github
3. Upload the gear_control, testing_interface, osrf_gear and universal_robot folders in the AWS Robomaker instance. 
4. Make a new folder named rqt which will be a robot application to display rqt_console.
5. Open a new terminal. 
    `$ sudo su`
    `$ source /opt/ros/melodic/setup.bash` 
    `$ colcon build` 
    `$ colcon bundle` 
6. Upload the bundle file output.tar to the S3 bucket. 
    `$ aws s3 cp /bundle/output.tar s3://<name of S3 bucket>/output.tar`

7. Create robot application. 
    `$ aws robomaker create-robot-application --name <name of robot application> --sources  s3Bucket=<name of S3 bucket>, s3Key= output.tar, architecture=X86_64 --robot-software-suite  name=ROS, version=Melodic`  

8. Create simulation application 
    `$ aws robomaker create-simulation-application --name <name of simulation application> -- sources s3Bucket=<name of S3 bucket>,s3Key=output.tar, architecture=X86_64 --robot-software-suite  name=ROS, version=Melodic --simulation-software-suite name=Gazebo, version=9 --rendering-engine  name=OGRE, version=1.x`

9.  Click on Simulation Jobs on left panel. 
10. Click on Create simulation job.
11. In configure simulation window choose simulation job duration. 
12. Choose Failure behavior as continue. 
13. Choose ROS distribution as Melodic. 
14. Choose IAM role. 
15. Select the job output as the S3 bucket.
16. In Specify Robot Application select `choose existing application`. 
17. Choose the robot application in dropdown list i.e., rqtconsole. 
18. Type the launch package name as robot_app. 
19. Type the launch file name as rqt.launch. 
20. Enable Run with streaming session. 
21. In Specify Simulation Application select `choose existing application`. 
22. Choose the simulation application in dropdown list. 
23. Type the launch package name as osrf_gear. 
24. Type the launch file name as sample_environment.launch 
25. Enable Run with streaming session. 
26. In create and review click on create. 
27. When the status shows Running connect to simulation Application to view the interface GUI  application and connect to GZClient to see the simulation running in the gazebo. Also connect to Robot  application to view the rqt_console. 
28. The error logs can be viewed on clicking logs link which is directed to AWS CloudWatch service.


## Tools Used 🛠️
* ROS
* Gazebo
* PyQt
* AWS RoboMaker



## License 📄
This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE) file for details.