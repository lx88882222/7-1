'''
> sensor node
> subscribe the message of ultrasonic sensor
>   author:whf
>   date:2024-05-18
> attribute:
    self.dist (float)
>   do obstacle avoidance in sensor node: if dist < 0.9, call self.avoid(), otherwise do nothing.
>   avoid(self):only change speed_z now TODO
'''
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd
import time
from .constants import C
class ultrasonic(Node):
    '''subscribe the message of sensor'''
    def __init__(self) -> None:
        super().__init__('sensor_mode')
        self.dist=0.0
        self.sub = self.create_subscription(Range, f'/{C.NAME}/ultrasonic_payload', self.sub_callback, 10)
        self.cmd_pub = self.create_publisher(MotionServoCmd, f"/{C.NAME}/motion_servo_cmd", 10)
    def sub_callback(self, msg: Range):
        '''the callback function of subscriber'''
        if msg.range is None:
            pass
        else:
            self.dist=msg.range
        self.get_logger().info(f"the distance is {self.dist}")
        if self.dist > C.AVOID_DIST:
            pass
        else:
            self.avoid()
    def avoid(self):
    # 如果距离小于90cm，则开转
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.5
        self.get_logger().info(f"距离小于90cm，the distance is {self.dist}")
        msg = MotionServoCmd()
        msg.motion_id = 308
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05,0.05]
        self.cmd_pub.publish(msg)