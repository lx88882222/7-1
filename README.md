# 7-1
7-1汪汪汪

## 信息
### 配置
#### 狗
+ 7-1  
    IP:10.0.0.168  
    password：123
    namespace：az1
+ 7-2
    IP：10.0.0.124  
    password：123   
    namespace：az  
    tightVNC：  
        Remote Host：10.0.0.123:5901  
        password：az888888 
上位机 10.0.0.144
[VScode配ssh--bilibili教程前三分钟](https://www.bilibili.com/video/BV1Ld4y1M7EV/?share_source=copy_web&vd_source=b987eb909065c989d772c8c7a783e243)

#### 狗
7-1 & 7-2  
名字:az 
### 提醒
+ 同时写代码时注意保存
+ build之前要先在终端输入`cd workplace`,否则无法更新所做的修改!
+ 单独编译某一个包 colcon build --packages-select learning
+
### 参考资料
#### 二代机器狗的开源信息：
1. [文档博客](https://miroboticslab.github.io/blogs/#/)
2. [源码地址](https://github.com/MiRoboticsLab/cyberdog_ws)

#### ROS学习参考
1. [发布订阅节点](https://blog.csdn.net/qq_38649880/article/details/104423203)
2. 
#### 其它资料
1. [第一次培训的PPT和录屏](https://cloud.tsinghua.edu.cn/d/1d9eadb6263f4e75aaff/)
2. [第二次培训的PPT和录屏](https://cloud.tsinghua.edu.cn/d/9aefef66ac9542a6944d/)
3. [代码托管](https://git.tsinghua.edu.cn/cyberdog_competition/2024)
4. [whf的github仓库](https://github.com/HeFeiW/cyberdog_az)
## 进度
#### todo：
+ 四段式  
    - 上位机：球门坐标，球坐标，前锋坐标，计算延长线，最短路线走至距球一定距离
    - 摄像头：原地角度旋转，检测x坐标位于画面中央（x==320）
    - 摄像头/深度相机：后退一定距离
    - 摄像头/深度相机：快走【一定时间】踢球
+ socket  
    - 
+ bash
+ 检查 7-1 7-2 白狗的rgb_cam返回图像大小，是640*480还是500*400？
+ 用7-1中ai photo拍摄比赛场地内狗和球的图像，并进行数据标注[数据标注参考视频](https://www.bilibili.com/video/BV1234y137Mt/?share_source=copy_web&vd_source=255f48a582c856914da3baa72f8c394a),百度智能云，roboflow，云服务器？
### 进度记录
#### 04.23 李想 何冠奇 王鹤霏
+ 主要是尝试理解了一下ros2的工作机制: subscribe & publish / server & client
+ 修改了walk.py,实现在执行小步慢走的同时向终端返回distance,但没有实现实时更新distance
+ 帮大家踩了一个大坑(bushi)
#### 05.02 李想 王鹤霏
+ 进度：无 精神状态：凉好
+ 尝试source bash失败（每次启动terminal重新执行activate，耗时长，且启动过一次后在尝试启动会transitioning failed）；输入命令行后rgb相机打不开，topic echo无返回值。
#### 05.03 李想
+ 解决了莫名其妙进入虚拟环境的问题（卸载VScode python插件）
+ 解决了（至少在一次调试里成功了。。）rgb相机打不开，/image_rgb主题echo不回来数据的问题
+ 实现了rgb相机publish出去的/image_rgb话题的订阅，并且成功在电脑上可视化。（需要在电脑上下载Xming软件并配置，需要在狗的.bashrc文件里配置）
+ 成功一次后，重启后仍然存在相机打不开的问题，不知道哪里出现了问题。。。
+ 抱了自01 胡振桦学长的大腿 感谢他
#### 05.04 李想
+ 
### 常用命令行
<!-- 1. 打开相机： 
    + ros2 launch realsense2_camera on_dog.py
    + ros2 lifecycle set /camera/camera configure
    + ros2 lifecycle set /camera/camera activate -->
1.打开realsense(研究中......)
    + ros2 launch realsense2_camera on_dog.py
    + ros2 launch realsense2_camera realsense_align_node.launch.py
    + ros2 lifecycle set /az1/camera/camera configure
    + ros2 lifecycle set /az1/camera/camera activate
    + ros2 lifecycle set /az1/camera/camera_align configure
    + ros2 lifecycle set /az1/camera/camera_align activate
    + ros2 service call /on_dog/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}"
    + ros2 service call /realsense2_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}"

    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}"
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}"

2. 运行
    + cd workplace
    + colcon build
    + ros2 run learning XXX
3. 启动rgb相机
    + 窗口1:ros2 launch camera_test stereo_camera.py
    + 窗口2:# 启动lifecycle的接口
    + ros2 lifecycle set /az1/camera/camera configure 
    + ros2 lifecycle set /az1/camera/camera activate 
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}" 
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}"
4. 连接Xming
    + export DISPLAY=local ip:0.0
        + xhost +
5. 检查是否连接成功
    + ros2 topic list
    + ros2 topic echo /<名称>
### 运动参数
飞扑距离
x==410,y==378,area==31450
上位机：
摄像头坐标系，左-右+，球门y坐标7.9 x坐标0.2

#### 如何配置Xming实现远程主机（Windows）屏显
##### 远程主机（自己的电脑，此处用的是Windows）
+ 下载Xming[下载网址](https://sourceforge.net/projects/xming/?source=typ_redirect)
+ 打开Xming安装目录，目录下x0.hosts文件，在localhost下另起一行粘贴入{本机IP}（10.0.0.123/168），保存
+ 如果在上一步之前打开过Xming，要关闭后重启
+ 远程配置完毕
+ 查看【远程IP】：WindowsPowershell输入ipconfig查看局域网IPv4 ip地址（10.0.0.xxx）
+ 
##### 本机（此处为狗子的linux系统）  
+ sudo apt-get install x11-xserver-utils
+ xstart（只需执行一次，之后重启狗子无需再执行，下面其余命令在重启后要重新执行）
+ export DISPLAY={远程IP}:0.0
+ xhost +
\* 切换rgb相机传回图像类别：/opt/ros2/cyberdog/share/camera_test/config（注意**不在**/home/mi目录下，要在open folder那边直接复制上面路径）下yaml文件，修改format_rgb参数（改为rgb对应选项）

### issue
球和球门垂直


### debug记录&提醒
+ 如果转速过大，狗子转的角度会大于预设角度
+ 打开src中的learning而非install中的learning
+ build或者git的时候记得cd

#### 规则及分析
1. 总体：  
两方红黑狗对攻  
2. 避障：  
避障线程+striker线程，避障线程在发出避障指令前判断：目前是否在射门中，若在射门中，则不发出指令。
加一个topic，记录当前状态（strike or avoid）。
3. 守门：  

4. striker：  
射门
    转到直线
    优先靠近球，再yz旋转至正确射门方向
防守

2. 如何防止踢球时卡球：  
更改rotate函数使球不处于正中间

#### 在ros2中新建功能包
`cd workpalce/src    //先cd到工作空间的src里`
`ros2 pkg create --build-type ament_python <pkg_name>    //如果是c语言，ament_python 改为 ament_cmake`
生成的功能包结构：
```bash
  -src
    -pkg_name
        -_init.py
    -resource
    -test
    -package.xml
    -setup.cfg
    -setup.py
```
+ build功能包：  
`colcon build --packages-select <pkg_name>   //注意要在workplace里build`
+ 初次build前记得source一下，不然会报错package not found
`source ~/workplace/install/setup.bash`

translate aim ball 如果出视野 优先查上位机，如果上位机长时间不想答应，转到rotate模式，
todo:避障
