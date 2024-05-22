'''

'''
import rclpy
from rclpy.node import Node
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

def main(args=None):
    rclpy.init(args=args)
    striker_node = striker_node()
    striker_node.start()
    rclpy.spin(striker_node)
    striker_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()