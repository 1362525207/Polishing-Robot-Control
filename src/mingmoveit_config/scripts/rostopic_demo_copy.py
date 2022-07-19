#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree.ElementTree import PI
from geometry_msgs.msg import Pose
from trajectory_msgs.msg import *
from control_msgs.msg import *
import rospy
import actionlib
from sensor_msgs.msg import JointState
pi=3.14159265
JOINT_NAMES = ['zhixianmove', 'zhuan1', 'zhuan2',
               'zhuan3', 'zhuan4', 'zhuan5']
 



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

def move():
    #goal就是我们向发送的关节运动数据，实例化为FollowJointTrajectoryGoal()类
    file = "/home/mhq/mingurdf2/src/nurbs/sum.txt"
    f = loadData(file)
    goal = FollowJointTrajectoryGoal()
    arm_goal  = [0, 0, 0, 0, 0, 0]

    # 使用设置的目标位置创建一条轨迹数据，先回到初始位置
    arm_trajectory = JointTrajectory()
    arm_trajectory.joint_names = JOINT_NAMES

    arm_trajectory.points.append(JointTrajectoryPoint())
    arm_trajectory.points[0].positions = arm_goal
    arm_trajectory.points[0].velocities = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[0].accelerations = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[0].time_from_start = rospy.Duration(3.0)

    arm_trajectory.points.append(JointTrajectoryPoint())
    arm_goal  = [f[0][0], f[1][0], -f[2][0], -f[3][0], -f[4][0], 0]
    arm_trajectory.points[1].positions = arm_goal
    arm_trajectory.points[1].velocities = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[1].accelerations = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[1].time_from_start = rospy.Duration(6.0)
    time=6.0
    now=2
    for i in range(0,27,1):
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [f[0][i], f[1][i], -f[2][i], -f[3][i], -f[4][i], 0]
        arm_trajectory.points[now].positions = arm_goal
        if i<2 & i>=1:
            arm_trajectory.points[now].velocities = [0.039*i for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [0.039 for inow in JOINT_NAMES]
        elif (i<27 & i>=25):
            arm_trajectory.points[now].velocities = [((26-i)*0.039) for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [-0.039 for inow in JOINT_NAMES]
        else:
            arm_trajectory.points[now].velocities = [0.05 for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [0 for inow in JOINT_NAMES]
        arm_trajectory.points[now].time_from_start = rospy.Duration(0.1+time)
        time=time+0.1
        now=now+1
        #wpose.position.x = f[0][i] - 0.01
    
    arm_trajectory.points.append(JointTrajectoryPoint())
    arm_goal  = [f[0][27], f[1][27], -f[2][27], -f[3][27], -f[4][27], 0]
    arm_trajectory.points[now].positions = arm_goal
    arm_trajectory.points[now].velocities = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[now].accelerations = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[now].time_from_start = rospy.Duration(time+3)
    time=time+3
    now=now+1

    for i in range(27,54,1):
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [f[0][i], f[1][i], -f[2][i], -f[3][i], -f[4][i], 0]
        arm_trajectory.points[now].positions = arm_goal
        if (i-27)<2 & (i-27)>=1:
            arm_trajectory.points[now].velocities = [0.039*(i-27) for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [0.039 for inow in JOINT_NAMES]
        elif (i<54 & i>=52):
            arm_trajectory.points[now].velocities = [((53-i)*0.039) for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [-0.039 for inow in JOINT_NAMES]
        else:
            arm_trajectory.points[now].velocities = [0.05 for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [0 for inow in JOINT_NAMES]
        arm_trajectory.points[now].time_from_start = rospy.Duration(0.1+time)
        time=time+0.1
        now=now+1

    arm_trajectory.points.append(JointTrajectoryPoint())
    arm_goal  = [f[0][54], f[1][54], -f[2][54], -f[3][54], -f[4][54], 0]
    print(arm_goal)
    arm_trajectory.points[now].positions = arm_goal
    arm_trajectory.points[now].velocities = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[now].accelerations = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[now].time_from_start = rospy.Duration(time+3)
    time=time+3
    now=now+1

    for i in range(54,81,1):
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [f[0][i], f[1][i], -f[2][i], -f[3][i], -f[4][i], 0]
        arm_trajectory.points[now].positions = arm_goal
        if (i-54)<2 & (i-54)>=1:

            arm_trajectory.points[now].velocities = [0.039*(i-54) for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [0.039 for inow in JOINT_NAMES]
        elif (i<81 & i>=79):
            arm_trajectory.points[now].velocities = [((80-i)*0.039) for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [-0.039 for inow in JOINT_NAMES]
        else:
            arm_trajectory.points[now].velocities = [0.05 for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [0 for inow in JOINT_NAMES]
        arm_trajectory.points[now].time_from_start = rospy.Duration(0.1+time)
        time=time+0.1
        now=now+1

    arm_trajectory.points.append(JointTrajectoryPoint())
    arm_goal  = [f[0][81], f[1][81], -f[2][81], 2*pi+f[3][81], -f[4][81], 0]
    arm_trajectory.points[now].positions = arm_goal
    arm_trajectory.points[now].velocities = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[now].accelerations = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[now].time_from_start = rospy.Duration(time+3)
    time=time+3
    now=now+1

    for i in range(81,108,1):
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_goal  = [f[0][i], f[1][i], -f[2][i], 2*pi+f[3][i], -f[4][i], 0]
        arm_trajectory.points[now].positions = arm_goal
        if (i-81)<2 & (i-81)>=1:
            arm_trajectory.points[now].velocities = [0.039*(i-81) for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [0.039 for inow in JOINT_NAMES]
        elif (i<108 & i>=106):
            arm_trajectory.points[now].velocities = [((107-i)*0.039) for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [-0.039 for inow in JOINT_NAMES]
        else:
            arm_trajectory.points[now].velocities = [0.05 for inow in JOINT_NAMES]
            arm_trajectory.points[now].accelerations = [0 for inow in JOINT_NAMES]
        arm_trajectory.points[now].time_from_start = rospy.Duration(0.1+time)
        time=time+0.1
        now=now+1

    arm_trajectory.points.append(JointTrajectoryPoint())
    arm_goal  = [0, 0, 0, 0, 0, 0]
    arm_trajectory.points[now].positions = arm_goal
    arm_trajectory.points[now].velocities = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[now].accelerations = [0.0 for i in JOINT_NAMES]
    arm_trajectory.points[now].time_from_start = rospy.Duration(time+3)


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
