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
from cv_bridge import CvBridge
from .walk_t_sec import move_t_sec
from .rotate import rotate_aim_ball
from .goal import make_goal
from .data_receive import get_dog_address
from .routine import get_goal_coords
from .routine import get_routine
def main():
    rclpy.init()
    rotate_aim_ball()
    dist=1
    dog_coords, ball_coords = get_dog_address()
    goal_coords=get_goal_coords(ball_coords,dog_coords,gate_coords,dist)
    print(goal_coords[0],goal_coords[1])
    theta,goDist=get_routine(ball_coords,dog_coords,goal_coords)
    print(theta,goDist)
    move_t_sec(theta/0.2,2,0.2)
    move_t_sec(goDist/0.5,0,0.5)


