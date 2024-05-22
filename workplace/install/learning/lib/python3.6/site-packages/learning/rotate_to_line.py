'''
让狗转，直到球处于视野中心（实现方法：让绿球x坐标位于260-400间）
跟随球出视野方向旋转，
函数rotate_aim_ball(mode=0)，
mode=0：球处于中心，停止，返回True
mode=1:持续动态跟随，直到KeyBoardInterrupt，返回True
'''
import cv2

from rclpy.node import Node

from protocol.msg import MotionServoCmd
import rclpy
import threading
import time

from .rgb_cam_suber import RGBCamSuber
from get_loc import LocReciv
from .stop_node import stop
from .rotate import rotate_aim_ball
from .walk_t_sec import move_t_sec


def rotate_to_line(line,target,loc,error = 0.1):
    left = 0
    t = 0.3
    speed = 0.3
    rotate_aim_ball(0,left)
    while not loc.inplace(target,error):
        rotate_aim_ball(0)
        move_t_sec(t,1,speed)


    