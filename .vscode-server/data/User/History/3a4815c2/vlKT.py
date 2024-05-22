#---get rgb image from stereo camera---#

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time
class rgb_cam_suber(Node):
    '''subscribe the message of stereo camera'''
    def __init__(self, name) -> None:
        super().__init__(name)
        self.path = '/home/mi/Pictures/dog/'
        self.count = 0
        self.declare_parameter("dog_name", "az1")
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, '/image_left', self.sub_callback, 10)
        pass

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        self.count += 1
        cv_image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
        image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(f'{self.path}{self.count}.jpg', image)
        self.get_logger().info(f'{self.count}.jpg saved successfully.')
        self.get_logger().info(f'the width of the image is {msg.width},height is {msg.height}')
        time.sleep(1)

def main(args=None):
    rclpy.init(args=args)
    node = rgb_cam_suber("rgb_cam_suber")
    rclpy.spin_once(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()