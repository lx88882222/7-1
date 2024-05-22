# -*- coding:utf-8 -*-
'''
>   get_loc.py
>   author: whf lx
>   date: 2024-5-11
>   receive data from the upper computer
>   start() function constantly receive data and update the instance's attributes
    start_in_thread() function run start() in thread
    get_data() function - receive data once and return the data (invalid date are directly returned as None)
                        - and keep record of 5 latest location info with timestamp
    attibutes:
        ball_coords: tuple, the coordinates of the ball, (x,y) (float)
        dog_coords: tuple, the coordinates of the dog
        ball_loc_rec: list, record of 5 latest ball location info with timestamp, [[timestamp(seconds, of e-3 precision),x,y],[[],[],[]],...]
        dog_loc_rec: the same as ball_loc_rec.
'''
import socket
import time
import threading

class LocReciv():
    def __init__(self) -> None:
        self.dog_name="az1"
        self.ip = '10.0.0.143' # 查看上位机ip，进行修改
        self.dalay = 0.1
        self.client_socket = socket.socket()
        self.client_socket.connect((self.ip, 40000))
        self.ball_coords=(.0,.0)
        self.dog_coords=(.0,.0)
        self.client_socket.send('start'.encode())
        self.ball_loc_rec = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.dog_loc_rec = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    def is_valid(loc):
        return loc[0] != None and loc[1] != None
    def get_data(self):
        self.client_socket.send('start'.encode())
        data = self.client_socket.recv(1024).decode()
        timestamp = time.time()
        # split方法用于按空格分隔字符串
        a, b, c, d = data.split(' ')
        # 将字符串转换为浮点数，如果字符串为'None'，则返回None
        a = float(a) if a != 'None' else None
        b = float(b) if b != 'None' else None
        c = float(c) if c != 'None' else None
        d = float(d) if d != 'None' else None
        self.ball_coords=(a,b)
        self.dog_coords=(c,d)
        if self.is_valid(self.ball_coords):
            self.ball_loc_rec.pop(0)
            self.ball_loc_rec.append([timestamp] + list(self.ball_coords))

        if self.is_valid(self.dog_coords):
            self.dog_loc_rec.pop(0)
            self.dog_loc_rec.append([timestamp] + list(self.dog_coords))
        
        return self.ball_coords, self.dog_coords

    def in_place(self,target,error):
        offset = (target[0]-self.dog_coords[0])*(target[0]-self.dog_coords[0]) + (target[1]-self.dog_coords[1])*(target[1]-self.dog_coords[1])
        return offset < error*error
    def start(self):
        self.client_socket.send('start'.encode())
        while True:
            self.get_data()
            self.get_logger().info(f"ball[{self.ball_loc_rec[4]}]\ndog[{self.dog_loc_rec[4]}]\n")
            time.sleep(self.delay)
    def start_in_thread(self):
        thread = threading.Thread(target=self.start)
        thread.start()

    