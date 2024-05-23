
'''
>   move_node.py
>   author: whf
>   date: 2024-05-22
>   All moving-related functions packed together.
>   funtions:
    - goto(self,target,frequency = 0.3)
>   all calculation are based on upper-computer coordinate system, velocity will be converted to dog coordinate system in func go().
from:move_to_target.py
    05/18 李想
    提供一个move到目标坐标的方法move_to(goal_address,socket).传入一个目标坐标和SocketReciv类示例
    目前步态是慢速步态，最大纵向速度0.65，最大横移速度0.3， 最大角速度1.25.
    注意必须输入浮点数
'''
import rclpy
import math
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import threading
import time
from .get_data import Location
from .stop_node import StopNode
from .rotate import rotate_aim_ball

class Move(Node):
    def __init__(self,name,location:Location,GATE,DIST):
        super().__init__(name)
        self.motion_id = 303
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        self.dog_name = "az1"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 1)
        self.arrived=False
        self.max_speed_x = 0.3
        self.max_speed_y = 0.65
        self.max_speed_z = 1.25
        self.GATE = GATE
        self.DIST = DIST
        self.location = location
    def goto(self,target,frequency = 0.3):
        '''
        goto(self,target:target_coords)
        go to point [target] at max speed.
        update movement cmd evert [frequency] seconds.
        '''
        print(f'going to{target}')
        while not self.location.in_place(target):
            my_loc = self.location.get_black_loc()   #   TODO red dog should chang tihs line
            v =self.max_vel(target,my_loc)
            vel = [v[0],v[1],.0]
            self.go(vel)
            time.sleep(frequency)
        print(f'targeting {target}, arrived at {self.location.black_dog}') 
        return True
    def go_for(self,duration,vel):
        '''
        go for [duration] seconds at speed [vel]
        vel:[speed+x,speed_y,speed_z]
        '''
        if duration != 0:
            print(f'going for {duration} seconds')
            current_time =time.time()
            while(time.time()-current_time<duration):
                 self.go(vel)
                 time.sleep(0.1)
            self.stop()
        if duration == 0:
            pass
        #   一直走。用while循环加订阅话题跳出
        return True


    def go(self,vel,motion_id = 303):
        '''
        一个比较方便的生成并发送cmd封装，输入vel三元列表即可
        '''
        msg = MotionServoCmd()
        msg.motion_id =motion_id
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [vel[1],-vel[0],vel[2]]
        print(f'vel:{msg.vel_des}')
        msg.step_height = [0.05,0.05]
        self.pub.publish(msg)
    
    def shoot(self,redundancy = 1.):
        '''
        shooting 
        go [redundancy] meters further
        '''
        rotate_aim_ball()
        duration = (self.DIST + redundancy)/self.max_speed_x
        self.go_for(duration,[self.max_speed_x,.0,.0])
    def max_vel(self,target,me):
        '''
        max_vel(self,target:target_coords,me: my_coords)
        return the max velocity pointing from me to target.
        '''
        vector = [.0,.0]
        dir = [1,1]
        vector[0]=target[0]-me[0]
        vector[1]=target[1]-me[1]
        dir = [vector[0]/abs(vector[0]),vector[1]/abs(vector[1])]
        vel_x = abs(self.max_speed_y * vector[0] / vector[1])
        if vel_x <= self.max_speed_x:
            vel = [dir[0] * vel_x,dir[1] * self.max_speed_y]
        else:
            vel = [dir[0] * self.max_speed_x , dir[1] * abs(self.max_speed_x * vector[1] / vector[0])]
        return vel 
    
def dist(point1, point2):
        distance = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
        return distance