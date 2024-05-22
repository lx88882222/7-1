'''
>   main.py
>   date:2024-5-11
'''
import rclpy
from .get_loc import Loc

def main(args=None):
    rclpy.init(args=args)
    location = Loc()
    location.start_in_thread()
    

if __name__ =='__main__':
    main()