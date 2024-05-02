import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd

class sensor_suber(Node):
    '''subscribe the message of sensor'''
    def __init__(self, name) -> None:
        super().__init__(name)

        self.declare_parameter("dog_name", "az")
        self.dist=0.0
        dog_name = self.get_parameter("dog_name").get_parameter_value().string_value
        self.sub = self.create_subscription(Range, f'/{dog_name}/ultrasonic_payload', self.sub_callback, 10)
         
    def sub_callback(self, msg: Range):
        '''the callback function of subscriber'''
        self.dist=msg.range
        self.get_logger().info(f"the distance is {self.dist}")

class basic_move(Node):
    def __init__(self, name, sensor_node):
        super().__init__(name)
        self.sensor_node = sensor_node
        self.speed_x, self.speed_y, self.speed_z = 0.1, 0.0, 0.0
        self.dog_name = "az"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        # self.count +=1
        # self.get_logger().info(f"the distance is {self.count}")

    def timer_callback(self):
        rclpy.spin_once(self.sensor_node)
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
        self.pub.publish(msg)
        self.get_logger().info(f"the distance is {self.sensor_node.dist}")

def main(args=None):
    rclpy.init(args=args)
    sensor_node = sensor_suber("my_sensor")
    move_node = basic_move("move_node", sensor_node)
    rclpy.spin_once(sensor_node)
    rclpy.spin(move_node)
    move_node.destroy_node()
    sensor_node.destroy_node()
    rclpy.shutdown()
