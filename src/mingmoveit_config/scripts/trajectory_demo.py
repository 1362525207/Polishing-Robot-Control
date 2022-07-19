#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class TrajectoryDemo():
    def __init__(self):
        rospy.init_node('trajectory_demo')
        
        # 是否需要回到初始化的位置
        reset = rospy.get_param('~reset', False)
        
        # 机械臂中joint的命名
        arm_joints = ['zhixianmove',
                      'zhuan1',
                      'zhuan2', 
                      'zhuan3',
                      'zhuan4',
                      'zhuan5']
        
        if reset:
            # 如果需要回到初始化位置，需要将目标位置设置为初始化位置的六轴角度
            arm_goal  = [0, 0, 0, 0, 0, 0]

        else:
            # 如果不需要回初始化位置，则设置目标位置的六轴角度 第三、四个值是相反的
            arm_goal  = [0, 0, 0, 0, 0, 0]

        # 连接机械臂轨迹规划的trajectory action server
        rospy.loginfo('等待手臂轨迹控制器...')       
        arm_client = actionlib.SimpleActionClient('arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
        arm_client.wait_for_server()        
        rospy.loginfo('联系中...')  
    
        # 使用设置的目标位置创建一条轨迹数据
        arm_trajectory = JointTrajectory()
        arm_trajectory.joint_names = arm_joints
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_trajectory.points[0].positions = arm_goal
        arm_trajectory.points[0].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[0].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[0].time_from_start = rospy.Duration(1.0)
        arm_goal  = [0, 4, 0, 0, 0, 0]
        arm_trajectory.points[1].positions = arm_goal
        arm_trajectory.points[1].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[1].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[1].time_from_start = rospy.Duration(5.0)
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [0, 0, 0, 0, 0, 0]
        arm_trajectory.points[2].positions = arm_goal
        arm_trajectory.points[2].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[2].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[2].time_from_start = rospy.Duration(8.0)

        rospy.loginfo('将手臂移动到目标位置 ....')
        
        # 创建一个轨迹目标的空对象
        arm_goal = FollowJointTrajectoryGoal()
        
        # 将之前创建好的轨迹数据加入轨迹目标对象中
        arm_goal.trajectory = arm_trajectory
        
        # 设置执行时间的允许误差值
        arm_goal.goal_time_tolerance = rospy.Duration(0.0)
    
        # 将轨迹目标发送到action server进行处理，实现机械臂的运动控制
        arm_client.send_goal(arm_goal)

        # 等待机械臂运动结束
        arm_client.wait_for_result(rospy.Duration(10))
        
        rospy.loginfo('....完成')
        
if __name__ == '__main__':
    try:
        TrajectoryDemo()
    except rospy.ROSInterruptException:
        pass
    
