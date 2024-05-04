import rclpy
import cv2
from rclpy.node import Node
from sensor_msgs.msg import Image

def main(args=None):
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Could not open camera")
        return
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        ret, frame = camera.read()
        if not ret or frame is None:
            print("Could not read frame from camera")
            break
        cv2.imshow("frame", frame)
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break
    camera.release()
    cv2.destroyAllWindows()