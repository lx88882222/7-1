#---get rgb image from stereo camera---#

import rclpy
import logging
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class rgb_cam_suber(Node):
    '''subscribe the message of stereo camera'''
    def __init__(self, name) -> None:
        super().__init__(name)
        self.bridge = CvBridge()
        self.declare_parameter("dog_name", "az")
        self.sub = self.create_subscription(Image, '/image_rgb', self.sub_callback, 10)
        pass

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        rgb_msg = msg
        self.get_logger().info(f"the width is {rgb_msg.width}, the height is {rgb_msg.height}")
        cv_image = self.bridge.imgmsg_to_cv2(rgb_msg, "bgr8")
        cv2.imwrite('rgb_image.jpg', cv_image)
        self.get_logger().info(f"the image has been saved")
        cv2.imshow("rgb_image", cv_image)
        cv2.waitKey(1)


def main(args=None):
    logging.info('hello')
    rclpy.init(args=args)
    node = rgb_cam_suber("rgb_cam_suber")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()