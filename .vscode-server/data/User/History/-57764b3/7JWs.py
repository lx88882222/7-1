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
    #   整个函数包在try里，这样 catch 异常并退出之前可以主动断开与上位机连接防止多次失败测试之后上位机过载。
    #   初始化
    GATE = [-0.2,8.8]
    DIST = 1.0
    __ERROR__ = 0.3
    NAME = 'az1'
    rclpy.init(args=args)
    rgb_cam_suber = RGBCamSuber('rgb_s')
    rclpy.spin_once(rgb_cam_suber)
    location = Location()
    print(f'where are we?')
    move = Move(NAME,location,GATE,DIST)
    try:
        # TODO 主循环，实际使用时可以改成 while True循环
        for i in range(5):
            print(f'-----in loop {i}-----')
            while time.time()-location.black_dog_loc_rec[4][0] > 1:
                #   确保当前自身位置信息是更新过的（上次时间戳距今小于 1s）
                print(f'latest rec at {location.black_dog_loc_rec[4][0]}')
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