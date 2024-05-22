import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import threading
import time

class MoveNode(Node):
    def __init__(self, name,mode):
        super().__init__(name)
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        if mode == 0:
            self.speed_x = 0.5
        elif mode == 1:
            self.speed_y = 0.5
        elif mode == 2:
            self.speed_z = 0.5
        self.dog_name = "az"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = MotionServoCmd()
        msg.motion_id = 308
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05,0.05]
        self.pub.publish(msg)

class StopNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        self.dog_name = "az"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = MotionServoCmd()
        msg.motion_id = 308
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05,0.05]
        self.pub.publish(msg)
def move_t_sec(t,mode):
    move_node = MoveNode("move_node",mode)
    stop_node = StopNode("stop_node")
    move_thread = threading.Thread(target=rclpy.spin, args=(move_node,))
    move_thread.start()
    time.sleep(t)
    stop_thread = threading.Thread(target=rclpy.spin, args=(stop_node,))
    stop_thread.start()
    time.sleep(0.1)
    move_node.destroy_node()
    stop_node.destroy_node()
    rclpy.shutdown()
def main(args=None):
    rclpy.init(args=args)
    move_t_sec(5,2)

if __name__ == "__main__":
    main()