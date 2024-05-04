#---get rgb image from stereo camera---#

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class rgb_cam_suber(Node):
      '''subscribe the message of stereo camera'''
      def __init__(self, name) -> None:
          super().__init__(name)

          self.declare_parameter("dog_name", "az1")

          dog_name = self.get_parameter("dog_name").get_parameter_value().string_value

          self.sub = self.create_subscription(Image, '/camera/infra2/image_rect_raw', self.sub_callback, 10)
          pass

      def sub_callback(self, msg: Image):
          '''the callback function of subscriber'''
          rgb_msg = msg
          self.get_logger().info(f"the width is {rgb_msg.width}, the height is {rgb_msg.height}")

def main(args=None):
    rclpy.init(args=args)
    node = rgb_cam_suber("rgb_cam_suber")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()