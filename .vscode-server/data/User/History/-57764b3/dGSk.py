'''
>   main.py
>   date:2024-5-11
'''
import rclpy
from .get_loc import Loc
from .geometry import Line

def main(args=None):
    gate_loc = [0.0,7.9]
    rclpy.init(args=args)
    location = Loc()
    location.start_in_thread()
    shot_line = Line()

if __name__ =='__main__':
    main()