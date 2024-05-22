'''
>   author: whf
>   date:2024-05-22
>   main node:
        always spin this node and do not create or destroy other nodes repeatedly
'''
import rclpy
from rclpy.node import Node
from .rgb_cam_suber import rgb_cam_suber
from .move_node import move
from .get_data import Location
from .routine import get_goal_coords
class main_node(Node):
    def __init__(self):
        super().__init__('az1_node')
        self.rgb_cam_suber = rgb_cam_suber('rgb_s')
        self.Move = move()

def main(args=None):
    rgb_cam_suber = rgb_cam_suber('rgb_s')
    Move = move()
    location = Location()
    rclpy.init(args=args)
    while True:
        location.get_data
        target = get_goal_coords(location.ball)
        

if __name__ == '__main__':
    main()