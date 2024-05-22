import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
from std_msgs.msg import String
from .sensor_node import sensor_suber
from .rgb_cam_suber import rgb_cam_suber
from .walk_t_sec import move_t_sec
from .rotate import rotate_aim_ball
from .goal import make_goal
from .data_receive import get_dog_address
from .routine import get_goal_coords
from .routine import get_routine

class striker_node(Node):
    def __init__(self, name, sensor_node):
        super().__init__(name)
        self.sensor_node = sensor_node
        self.cam_node = rgb_cam_suber('cam_striker')
        self.speed_x, self.speed_y, self.speed_z = 0.1, 0.0, 0.0
        self.dog_name = "az1"
        self.cmd_pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.phase_pub = self.create_publisher(String, f"/{self.dog_name}/phase", 1)
        
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
        self.cmd_pub.publish(msg)
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

def main():
    rclpy.init()
    rotate_aim_ball()
    dist=1
    dog_coords, ball_coords = get_dog_address()
    goal_coords=get_goal_coords(ball_coords,dog_coords,gate_coords,dist)
    print(goal_coords[0],goal_coords[1])
    theta,goDist=get_routine(ball_coords,dog_coords,goal_coords)
    print(theta,goDist)
    move_t_sec(theta/0.2,2,0.2)
    move_t_sec(goDist/0.5,0,0.5)
    rotate_aim_ball()
    make_goal()


