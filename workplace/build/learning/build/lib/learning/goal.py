'''
提供一个射门方法make_goal()
'''
from .walk_t_sec import move_t_se
import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import threading
import time

def make_goal():
    move_t_sec(1,0,-0.3)
    move_t_sec(3,0,1.0)
def main(args=None):
    make_goal()