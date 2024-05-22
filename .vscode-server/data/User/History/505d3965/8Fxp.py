
'''
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
    def __init__(self,name,GATE,DIST):
        super().__init__(name)
        self.motion_id = 303
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        self.dog_name = "az1"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 1)
        self.arrived=False
        self.max_speed_x = 0.65
        self.max_speed_y = 0.3
        self.max_speed_z = 1.25
        self.GATE = GATE
        self.DIST = DIST
        self.location = Location()
    def goto(self,target,frequency = 0.3):
        '''
        goto(self,target:target_coords)
        go to point target at max speed
        '''
        print(f'going to{target}')
        while not self.location.in_place(target):
            my_loc = self.location.black_dog   #   TODO red dog should chang tihs line
            v =self.max_vel(target,my_loc)
            vel = [v[0],v[1],.0]
            self.go(vel)
            time.sleep(frequency)
        print(f'targeting {target}, arrived at {self.location.black_dog}') 
        return True
    def go_for(self,duration,vel):
        if duration != 0:
            self.go(vel)
            time.sleep(duration)
            self.go([.0,.0,.0])
        if duration == 0:
            pass
        #   一直走。用while循环加订阅话题跳出
        return True


    def go(self,vel,motion_id = 303):
        msg = MotionServoCmd()
        msg.motion_id =motion_id
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = vel
        msg.step_height = [0.05,0.05]
        self.pub.publish(msg)
    
    def shoot(self):
        REDUNDANCY = 1.
        rotate_aim_ball()
        duration = (self.DIST + REDUNDANCY)/self.max_speed_x
        self.go_for(duration,[self.max_speed_x,.0,.0])
    def max_vel(self,target,me):
        '''
        max_vel(self,target:target_coords,me: my_coords)
        return the max velocity pointing from me to target.
        '''
        vector = [.0,.0]
        vector[0]=target[0]-me[0]
        vector[1]=target[1]-me[1]
        vel_y = self.max_speed_x * vector[1] / vector[0]
        if vel_y <= self.max_speed_y:
            vel = [self.max_speed_x,self.max_speed_x * vector[1] / vector[0]]
        else:
            vel = [self.max_speed_y * vector[0] / vector[1],self.max_speed_y]
        return vel 
    
    
    
    
    
    def timer_callback(self):
        _, dog_coords, _ = self.socket.get_data()
        delta_x = self.goal_address[0] - dog_coords[0]
        delta_y = self.goal_address[1] - dog_coords[1]
        speed_ratio = delta_y / delta_x if delta_x != 0 else float('inf')
        if dist(dog_coords,self.goal_address)>0.2:#如果没到，那么进行下一步
            if abs(speed_ratio) <= self.max_speed_x / self.max_speed_y:
            # 斜率小于最大允许斜率时，使用比例速度
                if delta_x>0:#目标点在狗的右边
                    self.speed_y = -0.3
                else :
                    self.speed_y = 0.3
                self.speed_x = -speed_ratio * self.speed_y
            elif abs(speed_ratio) <=6.5:#如果斜率大于最大允许斜率，但小于6.5，这说明狗和目标位置的横向距离已经足够接近
                if delta_x>0:#目标点在狗的右边
                    self.speed_y = -0.1
                else :
                    self.speed_y = 0.1
                self.speed_x = -speed_ratio * self.speed_y
            else:
                if delta_y>0:#目标点在狗的前方
                    self.speed_x=0.5
                else:
                    self.speed_x=-0.5
                self.speed_y=0.0
            
        else:
            self.arrived=True
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            
        self.get_logger().info(f"from {dog_coords}moving to {self.goal_address}")
        msg = MotionServoCmd()
        msg.motion_id = self.motion_id
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05,0.05]
        self.pub.publish(msg)



# def IsArrived(self,goal_coords):
#         _, dog_coords, _ = self.socket.get_data()
#         target_dist =dist(goal_coords,dog_coords)
#         if target_dist<0.2:#距离小于0.2视为到达
#             return True
#         else:
#             return False

def dist(point1, point2):
        distance = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
        return distance



def main(args=None): 
    s = SocketReciv()
    move_to([0.5, 6.1], s)
    move_to([-0.5, 6.1], s)
    move_to([0.5, 3.1], s)
    del s


if __name__ == "__main__":
    main() 