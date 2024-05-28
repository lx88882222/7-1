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
        self.LatestInfo = False
    def get_data(self):
        '''
        一定会得到一次data
        '''
        DATA_GOT = False
        while not DATA_GOT:
            self.client_socket.send('start'.encode())
            start  = time.time()
            try:
                print('trying...')
                data = self.client_socket.recv(1024).decode()
                print(f'time to get data: {time.time() - start}')
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
        print(f'self.my_loc = {self.my_loc()}')

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
        
        return self.ball, self.red_dog, self.black_dog
    
    
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
    def MayCrash(self,target):
        my_loc = self.my_loc()
        oppo_loc = self.oppo_loc()
        line = Line(my_loc,target,2)
        if not self.blockingWay(line,oppo_loc):
            print(f'wont crash set target {target} ')
            return target
        else:
            # vec1 = [target[0] - my_loc[0],target[1] - my_loc[1]]
            # vec2 = [oppo_loc[0] - my_loc[0],oppo_loc[1] - my_loc[1]]
            # crossProduct = vec1[0] * vec2[1] - vec1[1] * vec2[1]
            # if crossProduct > 0:
            try:
                vertic_line = Line(oppo_loc,-1/line.slope,1)
                if line.get_y(oppo_loc[0]) > oppo_loc[1]:
                    mode = 1
                else:
                    mode = -1
                NewTarget = vertic_line.get_target(C.SAFE_DIST,mode)
                if self.NotOut(NewTarget):
                    print(f'May crash, get new target:{NewTarget}')
                    return NewTarget
                else:
                    print(f'new target {NewTarget} out of filed')
                    NewTarget = vertic_line.get_target(C.SAFE_DIST,-mode)
                    print(f'shift target:{NewTarget}')
                    return NewTarget
            except Exception as e:
                print(f'Excepting occured in MayCrash, still go original path:{e}')
                return target
    def info_is_latest(self):
        current = time.time()
        ball_delay = current - self.ball_loc_rec[4][1]
        red_delay = current - self.red_dog_loc_rec[4][1]
        black_delay = current - self.black_dog_loc_rec[4][1]
        return ball_delay < C.INFO_DELAY and red_delay < C.INFO_DELAY and black_delay < C.INFO_DELAY
    
    def blockingWay(self,line,oppo_loc):
        print(line.slope)
        if C.SAFE_DIST * math.sqrt(line.slope * line.slope +1) < abs(line.slope * oppo_loc[0] - oppo_loc[1] + line.interception):
            # opponent is not close to target path
            return False
        vec1 = [line.point1[0]-oppo_loc[0],line.point1[1]-oppo_loc[1]]
        vec2 = [line.point2[0]-oppo_loc[0],line.point2[1]-oppo_loc[1]]
        if vec1[0] *vec2[0] + vec1[1] *vec2[1] > 0: # 两个向量成锐角 表示在target与my_loc为直径的圆周之外
            # opponent is close to target path but I wont go pass it
            return False
        return True
    def CanShoot(self,my_loc = None):
        self.get_data()
        if my_loc is None:
            my_loc = self.my_loc()
        shoot_line = Line(my_loc,self.ball,2)
        aim = shoot_line.get_x(C.GATE[1])
        if aim is None:
            return True #斜率小于0.05
        elif aim < C.GATE_RANGE[0]:
            return False   # 预期射门位置x偏小
        elif aim > C.GATE_RANGE[1]:
            return False    # 预期射门位置x偏大
        else:
            return True    # 预期射门位置在球门范围内
    def Scored(self):
        self.get_data()
        if self.ball[1] < C.GATE[1]:
            print('did not scored...')
            return False
        else:
            print('YEAAAAAAAH------')
            return True 
    def in_place(self,target,error = C.ERROR):
        self.get_data()
        offset = self.dist(target,self.my_loc())
        return offset < error      

    def my_loc(self):
        if self.color == 1:#black
            return self.black_dog
        if self.color == 0:#red
            return self.red_dog
    def oppo_loc(self):
        if self.color == 1:# im black
            return self.red_dog
        if self.color == 0:# im red
            return self.black_dog
    def my_loc_rec(self):
        if self.color == 1:#black
            return self.black_dog_loc_rec
        if self.color == 0:#red
            return self.red_dog_loc_rec
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
    def isLeft(self):#返回球在狗的左边还是右边， 1 for left, -1 for right
        if self.color == 1:#black
            if self.my_loc()[0] - self.ball[0] < 0:#球在黑狗左边
                return 1
            else:
                return -1
        elif self.color == 0:#red
            if self.my_loc()[0] - self.ball[0] > 0:#球在红狗左边
                return 1
            else:
                return -1 
    def dist(self,point1, point2):
        distance = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
        return distance
    
    def close(self):
        self.client_socket.close()
        print('socket connection closed.')

def main():
    location = Location()
    location.get_data()
    location.close()


if __name__ == "__main__":
    main()