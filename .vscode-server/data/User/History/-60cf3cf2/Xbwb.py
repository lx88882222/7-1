import rclpy
from rclpy.node import Node
from protocol.srv import MotionServoCmdService
from protocol.msg import MotionServoCmd

class BasicMoveService(Node):
    def __init__(self, name):
        super().__init__(name)
        self.dog_name = "az1"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.srv = self.create_service(MotionServoCmdService, f"/{self.dog_name}/motion_servo_cmd_service", self.motion_servo_cmd_callback)

    def motion_servo_cmd_callback(self, request, response):
        msg = MotionServoCmd()
        msg.motion_id = request.motion_id
        self.pub.publish(msg)
        return response

def main(args=None):
    rclpy.init(args=args)
    move_node = BasicMoveService("move_node")
    rclpy.spin(move_node)
    move_node.destroy_node()
    rclpy.shutdown()