#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geometry_msgs.msg import Pose
from trajectory_msgs.msg import *
from control_msgs.msg import *
import rospy
import actionlib
from sensor_msgs.msg import JointState
 
JOINT_NAMES = ['zhixianmove', 'zhuan1', 'zhuan2',
               'zhuan3', 'zhuan4', 'zhuan5']
 
def move():
    #goal就是我们向发送的关节运动数据，实例化为FollowJointTrajectoryGoal()类
    goal = FollowJointTrajectoryGoal()
    arm_goal  = [0, 0, 0, 0, 0, 0]
    arm_trajectory = JointTrajectory()
    arm_trajectory.joint_names = JOINT_NAMES
    arm_trajectory.points.append(JointTrajectoryPoint())
    arm_trajectory.points.append(JointTrajectoryPoint())
    arm_trajectory.points[0].positions = arm_goal
    #arm_trajectory.points[0].velocities = [0.0 for i in JOINT_NAMES]
    #arm_trajectory.points[0].accelerations = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[0].time_from_start = rospy.Duration(3.0)
    arm_goal  = [0, 0, 0, 4, 0, 0]
    arm_trajectory.points[1].positions = arm_goal
    arm_trajectory.points[1].velocities = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[1].accelerations = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[1].time_from_start = rospy.Duration(6.0)
    #goal当中的trajectory就是我们要操作的，其余的Header之类的不用管
    goal.trajectory = arm_trajectory
    goal.goal_time_tolerance = rospy.Duration(0.0)
    #goal.trajectory底下一共还有两个成员，分别是joint_names和points，先给joint_names赋值
    rospy.loginfo('过了成员了')
    #从joint_state话题上获取当前的关节角度值，因为后续要移动关节时第一个值要为当前的角度值
    #joint_states = rospy.wait_for_message("arm/joint_states",JointState)
    #joints_pos = joint_states.position
    #给trajectory中的第二个成员points赋值
    #points中有四个变量，positions,velocities,accelerations,effort，我们给前三个中的全部或者其中一两个赋值就行了
    #发布goal，注意这里的client还没有实例化，ros节点也没有初始化，我们在后面的程序中进行如上操作
    client.send_goal(goal)

    client.wait_for_result(rospy.Duration(6.0))
    rospy.loginfo('规划结束')
def pub_test():
    global client

    #初始化ros节点
    rospy.init_node("pub_action_test")
    #实例化一个action的类，命名为client，与上述client对应，话题为arm_controller/follow_joint_trajectory，消息类型为FollowJointTrajectoryAction
    client = actionlib.SimpleActionClient('/arm/arm_joint_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    print("Waiting for server...")
    #等待server
    client.wait_for_server()
    print("Connect to server")

    #执行move函数，发布action
    move()
 
if __name__ == "__main__":
    pub_test()
