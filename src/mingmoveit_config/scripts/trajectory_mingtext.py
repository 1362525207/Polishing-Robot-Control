#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import pi
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

pi=3.14159265

def loadData(fileName):
    inFile = open(fileName, 'r')
    #以只读方式打开某filename文件,该py文件是为了进行nurbs仿真测试的
    #定义2个空的list，用来存放文件中的数据
    gyrox = []
    gyroy = []
    gyroz = []
    gyroa = []
    gyrob = []
    for line in inFile:
        trainingSet = line.split('\t')#对于上面数据每一行，按' '把数据分开，这里是分成两部分
        gyrox.append(float(trainingSet[0]))#第五部分，即文件中的第五列数据逐一添加到list gyrox中
        gyroy.append(float(trainingSet[1]))#第六部分，即文件中的第六列数据逐一添加到list gyroy中
        gyroz.append(float(trainingSet[2]))#第七部分，即文件中的第七列数据逐一添加到list gyroz中
        gyroa.append(float(trainingSet[3]))#第六部分，即文件中的第六列数据逐一添加到list gyroy中
        gyrob.append(float(trainingSet[4]))#第七部分，即文件中的第七列数据逐一添加到list gyroz中
    inFile.close()
    return ( gyrox, gyroy, gyroz, gyroa, gyrob)


class TrajectoryDemo():
    def __init__(self):
        rospy.init_node('trajectory_demo')
        
        # 是否需要回到初始化的位置
        reset = rospy.get_param('~reset', False)
        file = "/home/mhq/mingurdf2/src/nurbs/sum.txt"
        f = loadData(file)
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
            # 如果不需要回初始化位置，则设置目标位置的六轴角度 第三、四、五个值是相反的
            arm_goal  = [0, 0, 0, 0, 0, 0]

        # 连接机械臂轨迹规划的trajectory action server
        rospy.loginfo('等待手臂轨迹控制器...')       
        arm_client = actionlib.SimpleActionClient('arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
        arm_client.wait_for_server()        
        rospy.loginfo('联系中...')  
    
        # 使用设置的目标位置创建一条轨迹数据，先回到初始位置
        arm_trajectory = JointTrajectory()
        arm_trajectory.joint_names = arm_joints
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_trajectory.points[0].positions = arm_goal
        arm_trajectory.points[0].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[0].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[0].time_from_start = rospy.Duration(3.0)

        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [f[0][0], f[1][0], -f[2][0], -f[3][0], -f[4][0], 0]
        arm_trajectory.points[1].positions = arm_goal
        arm_trajectory.points[1].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[1].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[1].time_from_start = rospy.Duration(6.0)
        time=6.0
        now=2
        for i in range(0,27,1):
            arm_trajectory.points.append(JointTrajectoryPoint())
            arm_goal  = [f[0][i], f[1][i], -f[2][i], -f[3][i], -f[4][i], 0]
            arm_trajectory.points[now].positions = arm_goal
            if i<2 & i>=1:
                arm_trajectory.points[now].velocities = [0.039*i for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [0.039 for inow in arm_joints]
            elif (i<27 & i>=25):
                arm_trajectory.points[now].velocities = [((26-i)*0.039) for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [-0.039 for inow in arm_joints]
            else:
                arm_trajectory.points[now].velocities = [0.05 for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [0 for inow in arm_joints]
            arm_trajectory.points[now].time_from_start = rospy.Duration(0.1+time)
            time=time+0.1
            now=now+1
            #wpose.position.x = f[0][i] - 0.01
        
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [f[0][27], f[1][27], -f[2][27], -f[3][27], -f[4][27], 0]
        arm_trajectory.points[now].positions = arm_goal
        arm_trajectory.points[now].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[now].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[now].time_from_start = rospy.Duration(time+3)
        time=time+3
        now=now+1

        for i in range(27,54,1):
            arm_trajectory.points.append(JointTrajectoryPoint())
            arm_goal  = [f[0][i], f[1][i], -f[2][i], -f[3][i], -f[4][i], 0]
            arm_trajectory.points[now].positions = arm_goal
            if (i-27)<2 & (i-27)>=1:
                arm_trajectory.points[now].velocities = [0.039*(i-27) for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [0.039 for inow in arm_joints]
            elif (i<54 & i>=52):
                arm_trajectory.points[now].velocities = [((53-i)*0.039) for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [-0.039 for inow in arm_joints]
            else:
                arm_trajectory.points[now].velocities = [0.05 for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [0 for inow in arm_joints]
            arm_trajectory.points[now].time_from_start = rospy.Duration(0.1+time)
            time=time+0.1
            now=now+1

        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [f[0][54], f[1][54], -f[2][54], -2*pi-f[3][54], -f[4][54], 0]
        print(arm_goal)
        arm_trajectory.points[now].positions = arm_goal
        arm_trajectory.points[now].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[now].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[now].time_from_start = rospy.Duration(time+3)
        time=time+3
        now=now+1

        for i in range(54,81,1):
            arm_trajectory.points.append(JointTrajectoryPoint())
            arm_goal  = [f[0][i], f[1][i], -f[2][i], -2*pi-f[3][i], -f[4][i], 0]
            arm_trajectory.points[now].positions = arm_goal
            if (i-54)<2 & (i-54)>=1:

                arm_trajectory.points[now].velocities = [0.039*(i-54) for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [0.039 for inow in arm_joints]
            elif (i<81 & i>=79):
                arm_trajectory.points[now].velocities = [((80-i)*0.039) for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [-0.039 for inow in arm_joints]
            else:
                arm_trajectory.points[now].velocities = [0.05 for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [0 for inow in arm_joints]
            arm_trajectory.points[now].time_from_start = rospy.Duration(0.1+time)
            time=time+0.1
            now=now+1

        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [f[0][81], f[1][81], -f[2][81], 2*pi+f[3][81], -f[4][81], 0]
        arm_trajectory.points[now].positions = arm_goal
        arm_trajectory.points[now].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[now].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[now].time_from_start = rospy.Duration(time+3)
        time=time+3
        now=now+1

        for i in range(81,108,1):
            arm_trajectory.points.append(JointTrajectoryPoint())
            arm_goal  = [f[0][i], f[1][i], -f[2][i], 2*pi+f[3][i], -f[4][i], 0]
            arm_trajectory.points[now].positions = arm_goal
            if (i-81)<2 & (i-81)>=1:
                arm_trajectory.points[now].velocities = [0.039*(i-81) for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [0.039 for inow in arm_joints]
            elif (i<108 & i>=106):
                arm_trajectory.points[now].velocities = [((107-i)*0.039) for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [-0.039 for inow in arm_joints]
            else:
                arm_trajectory.points[now].velocities = [0.05 for inow in arm_joints]
                arm_trajectory.points[now].accelerations = [0 for inow in arm_joints]
            arm_trajectory.points[now].time_from_start = rospy.Duration(0.1+time)
            time=time+0.1
            now=now+1

        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [0, 0, 0, 0, 0, 0]
        arm_trajectory.points[now].positions = arm_goal
        arm_trajectory.points[now].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[now].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[now].time_from_start = rospy.Duration(time+3)
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
        arm_client.wait_for_result(rospy.Duration(time+3))
        
        rospy.loginfo('....完成')
        
if __name__ == '__main__':
    try:
        TrajectoryDemo()
    except rospy.ROSInterruptException:
        pass
    
