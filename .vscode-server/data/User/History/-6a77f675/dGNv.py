# -*- coding:utf-8 -*-
import socket

# 建立socket连接



def get_dog_address():
    msg = 'start'
    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode()
    print(data)
def main():
    ip = '10.0.0.143' # 查看上位机ip，进行修改
    client_socket = socket.socket()
    client_socket.connect((ip, 40000))
    while True:
        get_dog_address()


if __name__ == '__main__':
    main()
    # 收到的消息格式如下'a b c d'，为一个字符串
    # 正常情况下字符串中是四个浮点数，依次由空格隔开，其中`a`为足球横轴左边，`b`为足球纵轴坐标，`c`为机器狗横轴坐标，`d`为机器狗纵轴坐标
    # 当无法识别到球或机器狗时，会拿到一个`None`，可以用如下方法分隔出需要的部分

    '''
    test_string = '0.5 0.9 None None'
    result = test_string.split(' ') # split方法用于按空格分隔字符串
    print(result)
    '''


