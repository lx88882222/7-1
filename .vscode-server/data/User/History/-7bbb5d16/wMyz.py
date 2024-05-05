import cv2
import rclpy
import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image

def detect_green_ball(image):
    '''Detect green ball in the image'''
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius > 10:  # you can change this value according to your need
            return (int(x), int(y), int(radius))
    return None

class rgb_cam_suber(Node):
    '''subscribe the message of stereo camera'''
    def __init__(self, name) -> None:
        super().__init__(name)
        self.bridge = CvBridge()
        self.declare_parameter("dog_name", "az1")
        self.sub = self.create_subscription(Image, '/image_rgb', self.sub_callback, 10)
        self.frame_count = 0
        self.tracker = cv2.TrackerCSRT_create()
        self.bbox = None

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        rgb_msg = msg
        self.get_logger().info(f"the width is {rgb_msg.width}, the height is {rgb_msg.height}")
        cv_image = self.bridge.imgmsg_to_cv2(rgb_msg, "bgr8")
        self.get_logger().info(f"the image has been saved")

        ball = detect_green_ball(cv_image)
        if ball is not None:
            x, y, r = ball
            self.bbox = (x - r, y - r, 2 * r, 2 * r)
            ok = self.tracker.init(cv_image, self.bbox)
        elif self.bbox is not None:
            ok, self.bbox = self.tracker.update(cv_image)
            if ok:
                p1 = (int(self.bbox[0]), int(self.bbox[1]))
                p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                cv2.rectangle(cv_image, p1, p2, (255,0,0), 2, 1)

        self.frame_count += 1
        cv2.putText(cv_image, f"Frame: {self.frame_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("rgb_image", cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = rgb_cam_suber("rgb_cam_suber")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()