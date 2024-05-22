import rclpy
import threading
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
        self.striker_thread = threading.Thread(target=self.strik,args=(self))
        # self.count +=1
        # self.get_logger().info(f"the distance is {self.count}")
    def strike(self):
        while True:
            rotate_aim_ball()
            dist=1
            dog_coords, ball_coords = get_dog_address()
            global gate_coords 
            gate_coords = (0.0,8.4)
            goal_coords=get_goal_coords(ball_coords,dog_coords,gate_coords,dist)
            print(goal_coords[0],goal_coords[1])
            theta,goDist=get_routine(ball_coords,dog_coords,goal_coords)
            print(theta,goDist)
            move_t_sec(theta/0.2,2,0.2)
            move_t_sec(goDist/0.5,0,0.5)
            rotate_aim_ball()
            make_goal()