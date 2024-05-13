'''
> stop_node.py
> define a class StopNode
    with attributes:
        stops any motion (sets all velocity to 0)
> define function stop()
set all velocity .0
    
'''
from protocol.msg import MotionServoCmd
from rclpy.node import Node
import rclpy

class StopNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        self.dog_name = "az"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = MotionServoCmd()
        msg.motion_id = 0
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05,0.05]
        self.pub.publish(msg)

def stop():
    rclpy.init(args=None)
    stop_node = StopNode("stop_node")
    rclpy.spin_once(stop_node)
    stop_node.destroy_node()