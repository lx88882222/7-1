import socket

class SocketReciv():
    def __init__(self) -> None:
        self.dog_name="az1"
        self.ip = '10.0.0.143' # 查看上位机ip，进行修改
        self.dalay = 0.1
        self.client_socket = socket.socket()
        self.client_socket.connect((self.ip, 40000))
        self.ball_coords=(.0,.0)
        self.dog_coords=(.0,.0)
        self.client_socket.send('start'.encode())

    def get_data(self):
        self.client_socket.send('start'.encode())
        data = self.client_socket.recv(1024).decode()
        # split方法用于按空格分隔字符串
        a, b, c, d = data.split(' ')
        # 将字符串转换为浮点数，如果字符串为'None'，则返回None
        a = float(a) if a != 'None' else None
        b = float(b) if b != 'None' else None
        c = float(c) if c != 'None' else None
        d = float(d) if d != 'None' else None
        self.ball_coords=(a,b)
        self.dog_coords=(c,d)
        return self.ball_coords, self.dog_coords

def main():
    s = SocketReciv()
    threading.Thread(target=s.receive).start()
    try:
        while(1):
            print(s.ball_coords)
            print(s.dog_coords)
            time.sleep(0.1)
    except KeyboardInterrupt:
        s.client_socket.close()
