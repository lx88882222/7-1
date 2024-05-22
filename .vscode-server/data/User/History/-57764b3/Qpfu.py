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
        GATE = [8.8,-0.2]
        DIST = 2.5
        rclpy.init(args=args)
        rgb_cam_suber = RGBCamSuber('rgb_s')
        rclpy.spin_once(rgb_cam_suber)
        location = Location()
        print(f'where are we?')
        move = Move('az1',location,GATE,DIST)
        for i in range(5):
            print(f'-----in loop {i}-----')
            location.get_data()
            target,_ = get_goal_coords(location.ball,location.black_dog,GATE,DIST)
            print(f'ball:{location.ball},me:{location.black_dog}')
            print(f'target is{target}')
            move.goto(target)
            move.shoot()
            print('successfully shoot!')
            print('sleeping...')
            time.sleep(5)
            print("Let's do it again!")
        rclpy.shutdown()
    except Exception as e:
        print(e)
        
    finally:
        location.close()
if __name__ == '__main__':
    main()