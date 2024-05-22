import socket
import threading
import time
class SocketReciv():
    def __init__(self) -> None:
        self.dog_name="az1"
        self.upper_ip = '10.0.0.144' # 查看上位机ip，进行修改
        self.dalay = 0.1
        self.client_socket = socket.socket()
        self.client_socket.connect((self.upper_ip, 40000))
        self.ball_coords=(.0,.0)
        self.red_dog_coords=(.0,.0)
        self.black_dog_coords=(.0,.0)
        self.client_socket.send('start'.encode())

    def get_data(self):
        self.client_socket.send('start'.encode())
        data = self.client_socket.recv(1024).decode()
        parts = data.split(' ')
        if len(parts) != 6:  # 确保我们有6个坐标值
            return False
        
        # 将字符串转换为浮点数，如果字符串为'None'，则返回None
        ball_coord = (float(parts[0]) if parts[0] != 'None' else None, float(parts[1]) if parts[1] != 'None' else None)
        red_dog_coord = (float(parts[2]) if parts[2] != 'None' else None, float(parts[3]) if parts[3] != 'None' else None)
        black_dog_coord = (float(parts[4]) if parts[4] != 'None' else None, float(parts[5]) if parts[5] != 'None' else None)
        if not None in ball_coord:
            self.ball_coords = ball_coord
        if not None in red_dog_coord:
            self.red_dog_coords = red_dog_coord
        if not None in black_dog_coord:
            self.black_dog_coords = black_dog_coord
        return self.ball_coords, self.red_dog_coords, self.black_dog_coords
    
    def receive(self):
        self.client_socket.send('start'.encode())
        while(1):
            self.get_data()
            time.sleep(self.dalay)
def main():
    s = SocketReciv()
    threading.Thread(target=s.receive).start()
    try:
        while(1):
            print(s.ball_coords)
            print(s.red_dog_coords)
            print(s.black_dog_coords)
            time.sleep(0.1)
    except KeyboardInterrupt:
        s.client_socket.close()
