'''
> sensor node
> subscribe the message of ultrasonic sensor

> attribute:
self.dist (float)

'''
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd
import time
class sensor_suber(Node):
    '''subscribe the message of sensor'''
    def __init__(self, name) -> None:
        super().__init__(name)

        self.declare_parameter("dog_name", "az1")
        self.dist=0.0
        dog_name = self.get_parameter("dog_name").get_parameter_value().string_value
        self.sub = self.create_subscription(Range, f'/{dog_name}/ultrasonic_payload', self.sub_callback, 10)
         
    def sub_callback(self, msg: Range):
        '''the callback function of subscriber'''
        self.dist=msg.range
        self.get_logger().info(f"the distance is {self.dist}")
    def avoid(self):
        if self.sensor_node.dist is not None and self.sensor_node.dist < 0.9:
            # 如果距离小于90cm，则开转
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.5
            self.get_logger().info(f"距离小于90cm，the distance is {self.sensor_node.dist}")
        if self.sensor_node.dist is not None and self.sensor_node.dist >= 0.9:
            # 如果距离大于90cm，则走
            self.speed_x, self.speed_y, self.speed_z = 0.3, 0.0, 0.0
            self.get_logger().info(f"距离大于90，the distance is {self.sensor_node.dist}")
        msg = MotionServoCmd()
        msg.motion_id = 308
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05,0.05]
        self.cmd_pub.publish(msg)
        self.get_logger().info(f"the distance is {self.sensor_node.dist}")
        time.sleep(0.1) 