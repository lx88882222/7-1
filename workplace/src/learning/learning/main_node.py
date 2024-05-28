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
import traceback
import sys
from .constants import C

def main(args=None):
    #   整个函数包在try里，这样 catch 异常并退出之前可以主动断开与上位机连接防止多次失败测试之后上位机过载。
    print(C.ERROR)
    rclpy.init(args=args)
    # rgb_cam_suber = RGBCamSuber('rgb_s')
    # rclpy.spin_once(rgb_cam_suber)
    location = Location()
    print(f'where are we?')
    move = Move(location)
    try:
        # TODO 主循环，实际使用时可以改成 while True循环
        for i in range(5):
            print(f'-----in loop {i}-----')
            while time.time()-location.my_loc_rec()[4][0] > 1:
                #   确保当前自身位置信息是更新过的（上次时间戳距今小于 1s）
                print(f'latest rec at {location.my_loc_rec()[4][0]}')
                location.get_data()
            target,_,shoot_mode= get_goal_coords(location.ball,location.my_loc(),C.GATE,C.DIST)
            print(f'ball:{location.ball},me:{location.my_loc()}')
            print(f'target is{target}')
            target = location.MayCrash(target)
            if not move.goto(target):
                continue
            # TODO check if ball_loc satisfies the requirements to shoot
            if not location.CanShoot():
                continue
            print(f'Can Shoot!')
            move.shoot(shoot_mode)
            print('successfully shoot!')
            print('sleeping...')
            if location.Scored():
                move.goto(C.START_POINT)
            print("Let's do it again!")
        rclpy.shutdown()
    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
    finally:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
        location.close()
if __name__ == '__main__':
    main()