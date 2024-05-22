from .walk_t_sec import move_t_sec
import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import threading
import time

def make_goal():
    move_t_sec(1,0,-0.3)
    time.sleep(0.01)
    move_t_sec(3,0,1.0)
def main(args=None):
    make_goal()