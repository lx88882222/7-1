'''

'''
import rclpy
from rcply.node import Node
from .rgb_cam_suber import rgb_cam_suber
from .walk_t_sec import MoveNode
class striker_node(Node):
    def __init__(self):
        super().__init__('striker_node')
        self.rgb_cam_suber = rgb_cam_suber('rgb_s')
        self.MoveNode = MoveNode('move_s')
    def start(self):
        self.rgb_cam_suber.start()
        self.MoveNode.start()