'''
守门狗
让狗沿x轴运动，直到球处于视野中心
mode=0：球处于中心，停止，返回True
mode=1:持续动态跟随，直到KeyBoardInterrupt，返回True
speed.y > 0 时往左走
'''
import cv2
import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image, Range
from protocol.msg import MotionServoCmd
import rclpy
import threading
import time
import socket
from .data_receive import get_dog_address


class rgb_cam_suber(Node):
    '''subscribe the message of stereo camera'''
    def __init__(self, name) -> None:
        super().__init__(name)
        self.bridge = CvBridge()
        self.declare_parameter("dog_name", "az1")
        self.sub = self.create_subscription(Image, '/image_rgb', self.sub_callback, 10)
        self.frame_count = 0
        self.size = 0
        self.ball_position = (0, 0)

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        rgb_msg = msg
        cv_image = self.bridge.imgmsg_to_cv2(rgb_msg, "bgr8")

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 43, 46])
        upper_green = np.array([77, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)

        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            self.size = cv2.contourArea(largest_contour)
            self.ball_position = (x, y)
            cv2.circle(cv_image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        if self.size <100:
            x,y = 0, 0
            self.ball_position = (x, y)
        # cv2.imshow("rgb_image", cv_image)
        cv2.waitKey(1)


class move_x(Node):
    def __init__(self, name, rgb_cam_suber):
        super().__init__(name)
        self.rgb_node = rgb_cam_suber
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        self.dog_name = "az1"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.x_rec=[320.0,320.0,320.0]
        self.size_rec=[.0,.0,.0,.0,.0]
        self.xx=[320.0,320.0,320.0]
        self.aim = False

        self.dog_coords, self.ball_coords = get_dog_address()
        self.ball_y_abs = self.ball_coords[1]
        self.ball_y_rec=[.0,.0,.0]



    def timer_callback(self):
        rclpy.spin_once(self.rgb_node)
        ball_x, ball_y = self.rgb_node.ball_position
        size = self.rgb_node.size

        if ball_x != 0:  # 持续更新x坐标
            self.x_rec.pop(0)
            self.x_rec.append(ball_x)
        self.size_rec.pop(0)
        self.size_rec.append(size)
        self.ball_y_rec.pop(0)
        self.ball_y_rec.append(self.ball_y_abs)

        avx=sum(self.x_rec)/len(self.x_rec)  
        avs=sum(self.size_rec)/len(self.size_rec)

        # self.xx.pop(0) # self.xx记录球的连续三个x值
        # self.xx.append(avx)

        # 如果球不见了或者球在往外走
        if (avs <= 500) | ((self.ball_y_rec[2]+0.1 < self.ball_y_rec[1]) & (self.ball_y_rec[1]+0.1 < self.ball_y_rec[0])): 
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            self.aim = False

        if (avs > 500) & (avs < 1600): # 如果球很远或者走掉了
            if  avx < 280: #球从左侧溜走:向左走  320是像素中心位置
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.27, 0.0
                if avx > 300:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            elif avx > 360: # 球从右侧溜走：向右走
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.27, 0.0
                if avx < 340:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            else:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        # 可以加一个校准系统：如果多次都在“中心”循环中，但是avoriginx偏差较大，就加一次速度
        
        if (avs >= 1600) & (avs < 1850): # 如果球比较近了
            # if yy[0]<yy[1] & yy[1]<yy[2]: # 如果球离球门越来越近
            if avx > 280 and avx < 360:  #球在视野中心：不再平移
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
                self.aim = True
            else:
                if (self.x_rec[0]+2.0 < self.x_rec[1]) & (self.x_rec[1]+2.0 < self.x_rec[2]): # 如果x越来越大，狗往右走
                    self.speed_x, self.speed_y, self.speed_z = 0.0, -0.35, 0.0
                elif (self.x_rec[2]+2.0 < self.x_rec[1]) & (self.x_rec[1]+2.0 < self.x_rec[0]):# 如果x越来越小，狗往左走
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.35, 0.0
                else: # 如果球几乎不动，狗不动
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
                    self.aim = True

        if (avs >= 1850) | (ball_y_abs > 7.9): # 如果球几乎在眼前
            if avx > 320:
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.45, 0.0
            else:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.45, 0.0

            
        # 下一步：利用左右相机，如果球在左边就疯狂往左走，反之亦然，除非size很小
        # 问题：如果球离狗很近，但是球在视野边缘，size也会很小，这时候就要用到上位机判断了

        msg = MotionServoCmd()
        if avs < 1600: 
            msg.motion_id = 308
        else: 
            msg.motion_id = 305 
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05, 0.05]
        self.pub.publish(msg)
        self.get_logger().info(f"ballyabs={self.ball_y_abs},avs={avs},size={size},avx={avx},origin_x={self.x_rec}")

   



def move_x_aim_ball(mode=0):
    rclpy.init()
    rgb_node = rgb_cam_suber("rgb_cam_suber")
    move_x_node = move_x("move_x_node", rgb_node)
    move_x_thread = threading.Thread(target=rclpy.spin, args=(move_x_node,))
    move_x_thread.start()
    if mode == 0:
        while(move_x_node.aim == False):
            pass
    elif mode == 1:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print('KeyBoardInterrupt')
    move_x_node.destroy_node()
    rgb_node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()
    return True
def main(args=None):
    print(move_x_aim_ball())
if __name__ == '__main__':
    main()