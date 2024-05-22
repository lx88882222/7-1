'''
守门狗
让狗沿x轴运动，直到球处于视野中心（实现方法：让绿球x坐标位于260-400间）
跟随球出视野方向旋转，
函数move_x_aim_ball(mode=0)，
mode=0：球处于中心，停止，返回True
mode=1:持续动态跟随，直到KeyBoardInterrupt，返回True
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
        self.x_rec=[.0,.0,.0,.0,.0]
        self.aim = False

    def timer_callback(self):
        rclpy.spin_once(self.rgb_node)
        ball_x, ball_y = self.rgb_node.ball_position
        size = self.rgb_node.size
        if ball_x != 0:  # 持续更新x坐标
            self.x_rec.pop(0)
            self.x_rec.append(ball_x)
        # 调整狗子距离球的位置
        # '''
        # # 溜走算法
        # if size < 100: # 如果球很远或者球走掉了
        #     av=sum(self.x_rec)/len(self.x_rec)  # 取一段时间的ballx坐标平均值
        #     if  av < 320: #球从左侧溜走
        #         self.speed_x, self.speed_y, self.speed_z = 0.2, 0.0, 0.0
        #     else: # 球从右侧溜走
        #         self.speed_x, self.speed_y, self.speed_z = -0.2, 0.0, 0.0
        # '''
        if size > 100:
            if ball_x > 260 and ball_x < 400:  #球在视野中心：不再平移
                self.speed_x = 0.0
                self.aim = True
            elif ball_x <= 260: #球在视野左侧
                self.speed_x, self.speed_y, self.speed_z = 0.2, 0.0, 0.0
            else: # 球在视野右侧
                self.speed_x, self.speed_y, self.speed_z = -0.2, 0.0, 0.0
        else:
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0

        msg = MotionServoCmd()
        msg.motion_id = 308
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05, 0.05]
        self.pub.publish(msg)
        self.get_logger().info(f"x={ball_x},arr={self.x_rec}move_x={self.speed_x}")

   



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