# -*- coding:utf-8 -*-
'''
>   get_data.py
>   author: whf
>   date: 2024-05-23
>   receive data from the upper computer
>   get_data() function - receive data once and return the data
                        - and keep record of 5 latest location info with timestamp
                        - if data is None, will not update nor report.
                        - keep requesting if received no data from upper-computer # TODO set [mode] to allow for quiting
    in_place(self,target,error = 0.3):
                        - if in place, return True, otherwise False.
                        - update data for once
    attibutes:
        ball: list, the coordinates of the ball, [x,y] (float)
        red_dog: list, the coordinates of the dog
        black_dog: list, the coordinates of the dog
        ball_loc_rec: list, record of 5 latest ball location info with timestamp, [[timestamp(seconds, of e-3 precision),x,y],[[],[],[]],...]
        red_dog_loc_rec: the same as ball_loc_rec
        red_dog_loc_rec: the same as ball_loc_rec
'''
import socket
import math
import time
from .constants import C
from .geometry import Line
class Location():
    def __init__(self) -> None:
        self.dog_name=C.NAME
        self.color = C.COLOR
        self.upper_ip = C.UPPER_IP # 查看上位机ip，进行修改
        self.upper_port = C.UPPER_PORT
        self.delay = 1
        self.client_socket = socket.socket()
        self.client_socket.settimeout(1)
        self.client_socket.connect((self.upper_ip, self.upper_port))
        self.ball=[.0,.0]
        self.red_dog=[.0,.0]
        self.black_dog=[.0,.0]
        self.ball_loc_rec = [[.0,.0,.0],[.0,.0,.0],[.0,.0,.0],[.0,.0,.0],[.0,.0,.0]]
        self.red_dog_loc_rec = [[.0,.0,.0],[.0,.0,.0],[.0,.0,.0],[.0,.0,.0],[.0,.0,.0]]
        self.black_dog_loc_rec = [[.0,.0,.0],[.0,.0,.0],[.0,.0,.0],[.0,.0,.0],[.0,.0,.0]]
    def get_data(self):
        DATA_GOT = False
        while not DATA_GOT:
            self.client_socket.send('start'.encode())
            try:
                print('trying...')
                data = self.client_socket.recv(1024).decode()
                DATA_GOT = True
            except socket.timeout:
                print('socket timeout, retry...')
                continue
        timestamp = time.time()
        parts = data.split(' ')
        if len(parts) != 6:  # 确保我们有6个坐标值
            return self.ball, self.red_dog, self.black_dog
        # 将字符串转换为浮点数，如果字符串为'None'，则返回None
        ball = [float(parts[0]) if parts[0] != 'None' else None, float(parts[1]) if parts[1] != 'None' else None]
        red_dog = [float(parts[2]) if parts[2] != 'None' else None, float(parts[3]) if parts[3] != 'None' else None]
        black_dog = [float(parts[4]) if parts[4] != 'None' else None, float(parts[5]) if parts[5] != 'None' else None]
        
        print(f'self.ball = {self.ball}')
        print(f'self.black_dog = {self.black_dog}')
        print('----------------')
        
        if not (None in ball):
            self.ball = ball
            self.ball_loc_rec.pop(0)
            self.ball_loc_rec.append([timestamp] + list(self.ball))
        if not (None in red_dog):
            self.red_dog = red_dog
            self.red_dog_loc_rec.pop(0)
            self.red_dog_loc_rec.append([timestamp] + list(self.red_dog))
        if not (None in black_dog):
            self.black_dog = black_dog
            self.black_dog_loc_rec.pop(0)
            self.black_dog_loc_rec.append([timestamp] + list(self.black_dog))
        self.NotOut(self.black_dog)   #TODO change for red dog
        return self.ball, self.red_dog, self.black_dog
    def in_place(self,target,error = C.ERROR):
        self.get_data()
        if self.color == 'red':
            loc = [self.red_dog_loc_rec[4][1],self.red_dog_loc_rec[4][2]]
        else:
            loc = [self.black_dog_loc_rec[4][1],self.black_dog_loc_rec[4][2]]
        offset = self.dist(target,loc)
        return offset < error
    def NotOut(self,loc):# TODO what to do if about to get out of the field? 
        if loc[0] < C.MARGIN[0][0]:
            # too left
            return False
        elif loc[0] > C.MARGIN[1][0]:
            # too right
            return False
        elif loc[1] > C.MARGIN[0][1]:
            # y too big
            return False
        elif loc[0] < C.MARGIN[1][1]:
            # y too small
            return False
        return True
    def crash(self,my_loc,target,oppo_loc):
        line = Line(my_loc,target)
        if C.SAFE_DIST * math.sqrt(line.slope * line.slope +1) > abs(line.slope * oppo_loc[0] - oppo_loc[1] + line.interception)
            # may crash if go the opt path

        return False
    def get_ball_loc(self):
        # self.get_data()
        loc = [self.ball_loc_rec[4][1],self.ball_loc_rec[4][2]]
        return loc
    def get_red_loc(self):
        # self.get_data()
        loc = [self.red_dog_loc_rec[4][1],self.red_dog_loc_rec[4][2]]
        return loc
    def get_black_loc(self):
        # self.get_data()
        loc = [self.black_dog_loc_rec[4][1],self.black_dog_loc_rec[4][2]]
        return loc
    def dist(self,point1, point2):
        distance = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
        return distance
    def close(self):
        self.client_socket.close()
        print('socket connection closed.')
