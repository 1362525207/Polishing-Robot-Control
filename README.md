# Polishing-Robot-Control
基于ROS系统的机械臂仿真，模拟运动控制卡的实现方式进行NURBS等插补算法仿真。基于launch文件以及xml语言进行相关定义以及开发，通过moveit!作为配置器，同时通过python脚本实现自定轨迹开发。

## 一、运动学模型：模型可以见pdf文档里面有三维构型
&emsp;&emsp;1）正运动学模型\
&emsp;&emsp;&emsp;&emsp;X=l1*sin(theta1)+l2*sin(theta1+theta2);\
&emsp;&emsp;&emsp;&emsp;Y=-l1cos(theta1)-l2*cos(theta1+theta2);\
&emsp;&emsp;&emsp;&emsp;Z=theta0*5（导程为5）+d基准坐标距离\
&emsp;&emsp;&emsp;&emsp;Beta=arcsin( (cos(theta4)+1)/2);\
&emsp;&emsp;&emsp;&emsp;Arpha=arctan((g2*sin(theta4))/(1-cos(theta4)))-theta1-theta2-theta3(g2是根号2)\
&emsp;&emsp;2）逆运动学模型\
&emsp;&emsp;&emsp;&emsp;Theta0=(z-d)/5;\
&emsp;&emsp;&emsp;&emsp;Theta1=arctan(y/x)-arctan((l2*sin(theta2))/(l2*cos(theta2)+l1))\
&emsp;&emsp;&emsp;&emsp;Theta2=arccos((x^2+y^2-l1^2-l2^2)/(2*l1*l2))\
&emsp;&emsp;&emsp;&emsp;Theta3=Arpha+theta1+theta2-arctan((g2*sin(theta4))/(1-cos(theta4)))\
&emsp;&emsp;&emsp;&emsp;Theta4=arccos(2*sin(beta)-1)\
&emsp;&emsp;3）空间限制\
&emsp;&emsp;1.主臂碰撞限制：\
&emsp;&emsp;&emsp;&emsp;对于末端的xy位置得到后：|kx-y|/(sqrt(k^2+1)) > 2.758*theta2-478.55\
&emsp;&emsp;&emsp;&emsp;即 260sin(theta2)-2.758*theta2+128.55>0&emsp;&emsp;&emsp;&emsp;单位都是角度单位，同时k是tan(theta1)\
&emsp;&emsp;2.y>0:\
&emsp;&emsp;&emsp;&emsp;轨迹规划的目标：建立两条曲线，因为一开始是与水平面夹角为90度，所以可以向左或者向右旋转，经过点的话则是趋向性，由负变到正这样。
## 二、程序说明
&emsp;&emsp;具体可见src文件夹：\
&emsp;&emsp;（1）moveit!设置：存在于mingmoveit_config文件夹，相关子结构图可以见设计说明；\
&emsp;&emsp;（2）urdf模型设置：存在于mingurdf文件夹，可以实现gazebo下的仿真；\
&emsp;&emsp;（3）运动仿真：存在于myrobot_control文件夹，可通过myrobot_trajectory.launch文件内部进行运动轨迹自定义；\
&emsp;&emsp;（4）ros_control配置：存在于roscontrol文件夹下，关于运动参数的设置。
## 三、使用说明
&emsp;&emsp;（1）简单使用：编译并刷新环境变量后运行：roslaunch mingurdf gazebo.launch\
&emsp;&emsp;（2）自定义轨迹：\
&emsp;&emsp;&emsp;&emsp;1.moveit!配置：src\mingmoveit_config文件夹下可以对yaml（系统参数）和launch（运行参数）进行相关修改；\
&emsp;&emsp;&emsp;&emsp;2.运动轨迹导入：src\myrobot_control\launch文件夹下有关轨迹的python连接脚本，可以直接运行相关脚本；
