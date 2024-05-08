import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd
import rclpy
import socket
import sys
import time
import cv2
import numpy as np

from .move_x import move_x_aim_ball

def main():
    move_x_aim_ball(mode=1)
