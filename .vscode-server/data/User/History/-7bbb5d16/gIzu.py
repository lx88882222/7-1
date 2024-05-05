import cv2
import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
import rclpy
import socket
import time


def get_dog_address():
    msg = 'start'
    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode()
    print(data)

class rgb_cam_suber(Node):
    '''subscribe the message of stereo camera'''
    def __init__(self, name) -> None:
        super().__init__(name)
        self.bridge = CvBridge()
        self.declare_parameter("dog_name", "az1")
        self.sub = self.create_subscription(Image, '/image_rgb', self.sub_callback, 10)
        self.frame_count = 0
        self.size=0

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        rgb_msg = msg
        # self.get_logger().info(f"the width is {rgb_msg.width}, the height is {rgb_msg.height}")
        cv_image = self.bridge.imgmsg_to_cv2(rgb_msg, "bgr8")

        # Convert BGR to HSV
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # define range of green color in HSV
        lower_green = np.array([35, 43, 46])
        upper_green = np.array([77, 255, 255])

        # Threshold the HSV image to get only green colors
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Find contours in the mask
        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour and assume this is the ball
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)

            # Calculate the size of the ball
            self.size = cv2.contourArea(largest_contour)
            print(f"The size of the ball is: {self.size}")

            # Draw the circle and centroid on the frame,
            cv2.circle(cv_image, (int(x), int(y)), int(radius), (0, 255, 255), 2)

        cv2.imshow("rgb_image", cv_image)
        cv2.waitKey(1)

def main(args=None):
    ip = '10.0.0.143' # 查看上位机ip，进行修改
    client_socket = socket.socket()
    client_socket.connect((ip, 40000))
    get_dog_address()
    get_dog_address()
    get_dog_address()
    rclpy.init(args=args)
    rgbnode = rgb_cam_suber("rgb_cam_suber")
    rclpy.spin(rgbnode)
    rgbnode.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()