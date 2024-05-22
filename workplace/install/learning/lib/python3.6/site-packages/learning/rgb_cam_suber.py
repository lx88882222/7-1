#---get rgb image from stereo camera---#
'''
>   author: all
>   rgb_cam_suber.py
>   define a class rgb_cam_suber(Node)
    with attributes:
        - bridge: CvBridge
        - sub: subscription to '/image_rgb'
        - frame_count: int
        - size: int
        - ball_position: tuple (float)
        - contour: list of numpy arrays, each array is a contour of the green area in image
        - size: the area of the biggest green area (when area < 100, assume that there's no green object in view, and ball position is set (0,0))

'''

import cv2
import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image

class RGBCamSuber(Node):
    '''subscribe the message of stereo camera'''
    def __init__(self, name) -> None:
        super().__init__(name)
        self.bridge = CvBridge()
        self.declare_parameter("dog_name", "az1")
        self.sub = self.create_subscription(Image, '/image_rgb', self.sub_callback, 10)
        self.frame_count = 0
        self.size = 0
        self.ball_position = (0, 0)

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        rgb_msg = msg
        cv_image = self.bridge.imgmsg_to_cv2(rgb_msg, "bgr8")

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 43, 46])
        upper_green = np.array([77, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)

        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            self.size = cv2.contourArea(largest_contour)
            self.ball_position = (x, y)
            cv2.circle(cv_image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        if self.size <100:
            x,y = 0, 0
            self.ball_position = (x, y)
        # cv2.imshow("rgb_image", cv_image)
        cv2.waitKey(1)