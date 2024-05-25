'''
>   author: whf
>   date:2024-05-22
>   main node:
        always spin this node and do not create or destroy other nodes repeatedly
'''

import rclpy
from .rgb_cam_suber import RGBCamSuber
from .move_node import Move
from .get_data import Location
from .routine import get_goal_coords
import time

def main(args=None):
    try:
        #   整个函数包在try里，这样 catch 异常并退出之前可以主动断开与上位机连接防止多次失败测试之后上位机过载。
        #   初始化
        GATE = [8.8,-0.2]
        DIST = 2.5
        rclpy.init(args=args)
        rgb_cam_suber = RGBCamSuber('rgb_s')
        rclpy.spin_once(rgb_cam_suber)
        location = Location()
        print(f'where are we?')
        move = Move('az1',location,GATE,DIST)
        # TODO 主循环，实际使用时可以改成 while True循环
        move.goto([0.0,4],1)
    except Exception as e:
        print(e)
        
    finally:
        location.close()
if __name__ == '__main__':
    main()