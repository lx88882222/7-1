from .walk_t_sec import move_t_sec
import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import threading
import time

def main(args=None):
    rclpy.init(args=args)
    move_t_sec(5,2)
    rclpy.shutdown()