import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd
from std_msgs.msg import Float32MultiArray

import cv2
import numpy as np
from cv_bridge import CvBridge


class sensor_suber(Node):
    '''subscribe the message of sensor'''
    def __init__(self, name) -> None:
        super().__init__(name)

        self.declare_parameter("dog_name", "az1")
        self.dist = None
        dog_name = self.get_parameter("dog_name").get_parameter_value().string_value
        self.sub = self.create_subscription(Range, f'/{dog_name}/ultrasonic_payload', self.sub_callback, 10)
         
    def sub_callback(self, msg: Range):
        '''the callback function of subscriber'''
        self.dist = msg.range
        self.get_logger().info(f"the distance is {self.dist}")

class basic_move(Node):
    def __init__(self, name, sensor_node, rgb_node):
        super().__init__(name)
        self.sensor_node = sensor_node
        self.rgb_node = rgb_node
        self.speed_x, self.speed_y, self.speed_z = 0.1, 0.0, 0.0
        self.dog_name = "az1"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.is_ball_centered = False

    def timer_callback(self):
        rclpy.spin_once(self.sensor_node)
        rclpy.spin_once(self.rgb_node)

        # 获取球的位置坐标
        ball_x, ball_y = self.rgb_node.ball_position

        # 当球在视野中心时，停止机器狗的旋转；否则一直旋转
        if self.is_ball_centered:
            self.speed_z = 0.0
        else:
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.5


        msg = MotionServoCmd()
        msg.motion_id = 308
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05, 0.05]
        self.pub.publish(msg)
        self.get_logger().info(f"the distance is {self.sensor_node.dist}")

    def ball_position_callback(self, msg):
        # RGB相机返回的球的位置坐标的回调函数
        self.is_ball_centered = False
        ball_x, ball_y = msg.data

        if ball_x > 200 and ball_x < 400 and ball_y > 150 and ball_y < 350:
            # 当球的位置在视野中心的范围内时，设置球在视野中心标志位为True
            self.is_ball_centered = True

def main(args=None):
    rclpy.init(args=args)
    sensor_node = sensor_suber("my_sensor")
    rgb_node = rgb_cam_suber("rgb_cam_suber")
    move_node = basic_move("move_node", sensor_node, rgb_node)
    rclpy.spin_once(sensor_node)
    rclpy.spin_once(rgb_node)
    rclpy.spin(move_node)
    move_node.destroy_node()
    sensor_node.destroy_node()
    rgb_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
