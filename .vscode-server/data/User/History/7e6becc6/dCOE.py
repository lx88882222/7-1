# -*- coding:utf-8 -*-
'''
>   get_data.py
>   author: whf
>   date: 2024-05-18
>   receive data from the upper computer
# >   start() function constantly receive data and update the instance's attributes
#     start_in_thread() function run start() in thread
    get_data() function - receive data once and return the data (invalid date are directly returned as None)
                        - and keep record of 5 latest location info with timestamp
    in_place(self,target,error = 0.3):if in place, return True, otherwise False.
    attibutes:
        ball_coords: tuple, the coordinates of the ball, (x,y) (float)
        dog_coords: tuple, the coordinates of the dog
        ball_loc_rec: list, record of 5 latest ball location info with timestamp, [[timestamp(seconds, of e-3 precision),x,y],[[],[],[]],...]
        dog_loc_rec: the same as ball_loc_rec.
'''
import socket
import threading
import time
class SocketReciv():
    def __init__(self) -> None:
        self.dog_name="az1"
        self.color = 'black'
        self.upper_ip = '10.0.0.144' # 查看上位机ip，进行修改
        self.delay = 1
        self.client_socket = socket.socket()
        self.client_socket.connect((self.upper_ip, 40000))
        self.ball_coords=(.0,.0)
        self.red_dog_coords=(.0,.0)
        self.black_dog_coords=(.0,.0)
        self.ball_loc_rec = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.red_dog_loc_rec = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.black_dog_loc_rec = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    def get_data(self):
        self.client_socket.send('start'.encode())
        data = self.client_socket.recv(1024).decode()
        timestamp = time.time()
        parts = data.split(' ')
        if len(parts) != 6:  # 确保我们有6个坐标值
            return self.ball_coords, self.red_dog_coords, self.black_dog_coords
        # 将字符串转换为浮点数，如果字符串为'None'，则返回None
        self.ball_coords = (float(parts[0]) if parts[0] != 'None' else None, float(parts[1]) if parts[1] != 'None' else None)
        self.red_dog_coords = (float(parts[2]) if parts[2] != 'None' else None, float(parts[3]) if parts[3] != 'None' else None)
        self.black_dog_coords = (float(parts[4]) if parts[4] != 'None' else None, float(parts[5]) if parts[5] != 'None' else None)
        self.ball_loc_rec.pop(0)
        self.ball_loc_rec.append([timestamp] + list(self.ball_coords))
        self.red_dog_loc_rec.pop(0)
        self.red_dog_loc_rec.append([timestamp] + list(self.red_dog_coords))
        self.black_dog_loc_rec.pop(0)
        self.black_dog_loc_rec.append([timestamp] + list(self.black_dog_coords))
        return self.ball_coords, self.red_dog_coords, self.black_dog_coords
    def in_place(self,target,error = 0.3):
        self.get_data()
        if self.color == 'red':
            loc = self.red_dog_coords
        else:
            loc = self.black_dog_coords
        offset = (target[0]-loc[0])*(target[0]-loc[0]) + (target[1]-loc[1])*(target[1]-loc[1])
        return offset < error*error
    def __del__(self):
        self.client_socket.close()
    # def receive(self):
    #     while(1):
    #         self.get_data()
    #         time.sleep(self.delay)
# def p(s:SocketReciv):
#     print('---s---')
#     try:
#         while(1):
#             print(s.ball_coords)
#             print(s.red_dog_coords)
#             print(s.black_dog_coords)
#             time.sleep(1)
#     except KeyboardInterrupt:
#         s.client_socket.close()
# def main():
#     print('编译成功')
#     s = SocketReciv()
#     t1 = threading.Thread(target=s.receive)
#     t1.start()
#     t2 = threading.Thread(target=p,args=(s))
#     t2.start()
    
