
'''
>   move_node.py
>   author: whf & lx
>   date: 2024-05-22
>   All moving-related functions packed together.
>   funtions:
    - goto(self,target,frequency = 0.3)
    - go_for(self,duration,vel)
>   all calculation are based on upper-computer coordinate system, velocity will be converted to dog coordinate system in func go().
from:move_to_target.py
    05/18 李想
    提供一个move到目标坐标的方法move_to(goal_address,socket).传入一个目标坐标和SocketReciv类示例
    目前步态是慢速步态，最大纵向速度0.65，最大横移速度0.3， 最大角速度1.25.
    注意必须输入浮点数
'''
import math
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import time
from .get_data import Location
from .rotate import rotate_aim_ball
from .constants import C
from .rgb_cam_suber import RGBCamSuber
import rclpy
import traceback
class Move(Node):
    def __init__(self,location:Location):
        super().__init__('move_node')
        self.dog_name = C.NAME
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 1)
        self.arrived=False
        self.max_speed_x = C.MAX_SPEED_X
        self.max_speed_y = C.MAX_SPEED_Y
        self.max_speed_z = C.MAX_SPEED_Z
        self.GATE = C.GATE
        self.DIST = C.DIST
        self.location = location
        self.rgb_node = RGBCamSuber("rgb_cam_suber")
    def goto(self,target,frequency = C.FREQUENCY):
        '''
        goto(self,target:target_coords)
        go to point [target] at max speed.
        update movement cmd evert [frequency] seconds.
        '''
        print(f'going to{target}')
        while not self.location.in_place(target):
            if self.rgb_node.CloseToBall():
                break
            v =self.max_vel(target,self.location.my_loc())
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

    def stop(self):
        '''
        stop the robot
        '''
        self.go([.0,.0,.0])
        return
    def go(self,vel,mode = 0):
        '''
        一个比较方便的生成并发送cmd封装，输入vel三元列表即可
        若mode缺省或为0，输入上位机坐标系下速度，在函数内映射为自身速度；
        若mode为 1 ，输入自身坐标系下速度。
        '''
        msg = MotionServoCmd()
        msg.motion_id =C.MOTION_ID
        msg.cmd_type = 1
        msg.value = 2
        if mode == 0:
            if C.COLOR == 0:    # RED
                msg.vel_des = [vel[1],-vel[0],vel[2]]
            elif C.COLOR == 1:
                msg.vel_des = [-vel[1],vel[0],vel[2]]
        else:
            msg.vel_des = vel
        print(f'vel:{msg.vel_des}')
        msg.step_height = C.STEP_HEIGHT
        self.pub.publish(msg)
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
    def rotate_aim_ball(self,mode=0,left=1):
        self.rgb_node = RGBCamSuber("rgb_cam_suber")
        if (1 == left):
            self.x_rec=[.0,.0,.0,.0,.0]
        else :
            self.x_rec=[640.,640.,640.,640.,640.]
        self.aim = False
        self.prefer_direc = left # 1 for left, -1 for right
        self.total_rotation = 0.0  #total rotation
        while self.aim is not True:
            rclpy.spin_once(self.rgb_node)
            ball_x, ball_y = self.rgb_node.ball_position
            size = self.rgb_node.size
            vel = [.0,.0,.0]
            if ball_x != 0:
                self.x_rec.pop(0)
                self.x_rec.append(ball_x)
            if size < 100:
                av=sum(self.x_rec)/len(self.x_rec)
                if av < 10:
                    vel = [0.0, 0.0, 0.5*self.prefer_direc]
                elif  av < 320:
                    vel = [0.0, 0.0, 0.5]
                else:
                    vel = [0.0, 0.0, -0.5]
            elif ball_x > 360 and ball_x < 420:
                vel = [.0,.0,.0]
                self.aim = True
                return self.total_rotation
            elif ball_x <= 360:
                vel = [0.0, 0.0, 0.25]
            else:
                vel = [0.0, 0.0, -0.25]
            self.total_rotation += vel[2] * 0.1  # 更新累积的角度，注意这里的0.1是时间间隔
            self.go(vel)
            self.get_logger().info(f"x={ball_x},arr={self.x_rec}rotate={vel[2]}")
            time.sleep(0.1)    
        return self.total_rotation
    def translate_aim_ball(self,left=1):
        if (1 == left):
            self.x_rec=[.0,.0,.0,.0,.0]
        else :
            self.x_rec=[640.,640.,640.,640.,640.]
        self.aim_horizontal = False
        self.prefer_direc_horizontal = left # 1 for left, -1 for right
        while self.aim_horizontal is not True:
            rclpy.spin_once(self.rgb_node)
            ball_x, ball_y = self.rgb_node.ball_position
            size = self.rgb_node.size
            if ball_x != 0:
                self.x_rec.pop(0)
                self.x_rec.append(ball_x)
            if size < 100:
                av=sum(self.x_rec)/len(self.x_rec)
                if av < 10:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.3*self.prefer_direc_horizontal, 0.0
                elif  av < 320:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.3, 0.0
                else:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, -0.3, 0.0
            elif ball_x > 380 and ball_x < 410:
                self.speed_y = 0.0
                self.aim_horizontal = True
                return
            elif ball_x <= 360:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.25, 0.0
            else:
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.25, 0.0
            self.go([self.speed_x,self.speed_y,self.speed_z],1)
            self.get_logger().info(f"translating,x={ball_x},arr={self.x_rec}")
            time.sleep(0.1)
        return True
        
    def shoot(self,mode=0,redundancy = 0.5):
        '''
        shooting
        Mode 0: Shoot from directly behind the football
        Mode 1: Rotate to face the ball and then shoot
        Mode 2: The ball is in the no-shooting zone on the left side of the field, move right to drag the ball to the shooting area and then shoot from directly behind
        Mode 3: The ball is in the no-shooting zone on the right side of the field, move left to drag the ball to the shooting area and then shoot from directly behind
        Mode 4: No shooting, do nothing

        go [redundancy] meters further
        '''
        if mode == 0:
            duration = (self.DIST + redundancy)/self.max_speed_x
            self.go_for(duration,[self.max_speed_x,.0,.0])
        elif mode == 1:
            ball_loc,my_loc = self.location.ball,self.location.my_loc()
            if(my_loc[0] - ball_loc[0] < 0):
                left = -1
            else:
                left = 1
            rotation=self.rotate_aim_ball(0,left)*1.1 #请别吐槽。。
            duration = (self.DIST + redundancy)/self.max_speed_x
            self.go_for(duration,[self.max_speed_x,.0,.0])
            if rotation>0:
                self.go_for(rotation/0.5,[.0,.0,-0.5])
            else:
                rotation = abs(rotation)
                self.go_for(rotation/0.5,[.0,.0,0.5])
        elif mode == 2:
            pass        
def dist(point1, point2):
        distance = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
        return distance