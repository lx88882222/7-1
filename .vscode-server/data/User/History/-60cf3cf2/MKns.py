import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd

class basic_move(Node):
    def __init__(self, name):
        super().__init__(name)
        self.dog_name = "az1"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        # self.count +=1
        # self.get_logger().info(f"the distance is {self.count}")

    def timer_callback(self):
        self.speed_x, self.speed_y, self.speed_z = 0.3, 0.0, 0.0
        msg = MotionServoCmd()
        msg.motion_id = 132
        # msg.cmd_type = 1
        # msg.value = 2
        # msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        # msg.step_height = [0.05,0.05]
        self.pub.publish(msg)
        # self.get_logger().info(f"the distance is {self.sensor_node.dist}")

def main(args=None):
    rclpy.init(args=args)
    move_node = basic_move("move_node")
    rclpy.spin_once(move_node)
    move_node.destroy_node()
    rclpy.shutdown()
