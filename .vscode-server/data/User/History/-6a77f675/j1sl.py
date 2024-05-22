# -*- coding:utf-8 -*-
import socket

def get_dog_address(client_socket):
    msg = 'start'
    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode()
    return parse_data(data)

def parse_data(data):
    # split方法用于按空格分隔字符串
    a, b, c, d = data.split(' ')
    # 将字符串转换为浮点数，如果字符串为'None'，则返回None
    a = float(a) if a != 'None' else None
    b = float(b) if b != 'None' else None
    c = float(c) if c != 'None' else None
    d = float(d) if d != 'None' else None
    # 返回两个坐标
    return (a, b), (c, d)

def main():
    ip = '10.0.0.143' # 查看上位机ip，进行修改
    client_socket = socket.socket()
    client_socket.connect((ip, 40000))
    goal_coords = (0.1, 7.9)  # 初始化球门坐标
    while True:
        ball_coords, dog_coords = get_dog_address(client_socket)
        dog_target_coords = get_dog_target_position(ball_coords, goal_coords)
        print(f"Ball coordinates: {ball_coords}, Dog coordinates: {dog_coords}, Dog target coordinates: {dog_target_coords}")

if __name__ == '__main__':
    main()