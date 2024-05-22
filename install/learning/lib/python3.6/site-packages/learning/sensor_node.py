'''
> sensor node
> subscribe the message of ultrasonic sensor

> attribute:
self.dist (float)

'''
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range

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