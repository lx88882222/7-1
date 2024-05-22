import socket

def get_dog_address():
    ip = '10.0.0.144'  # 查看上位机ip，进行修改
    client_socket = socket.socket()
    client_socket.connect((ip, 40000))
    msg = 'start'
    while True:
        client_socket.send(msg.encode())
        data = client_socket.recv(1024).decode()
        result = parse_data(data)
        if result is not False:
            return result

def parse_data(data):
    # 使用split方法按空格分隔字符串
    parts = data.split(' ')
    if len(parts) != 6:  # 确保我们有6个坐标值
        return False
    
    # 将字符串转换为浮点数，如果字符串为'None'，则返回None
    ball_coord = (float(parts[0]) if parts[0] != 'None' else None, float(parts[1]) if parts[1] != 'None' else None)
    red_dog_coord = (float(parts[2]) if parts[2] != 'None' else None, float(parts[3]) if parts[3] != 'None' else None)
    black_dog_coord = (float(parts[4]) if parts[4] != 'None' else None, float(parts[5]) if parts[5] != 'None' else None)

    # 如果任何一个坐标是None，返回False
    if None in ball_coord or None in red_dog_coord or None in black_dog_coord:
        return False
    
    # 返回三个坐标
    return ball_coord, red_dog_coord, black_dog_coord

def main():
    ball_coords, red_dog_coords, black_dog_coords = get_dog_address()
    print(f"Ball Coords: {ball_coords}")
    print(f"Red Dog Coords: {red_dog_coords}")
    print(f"Black Dog Coords: {black_dog_coords}")

if __name__ == '__main__':
    main()
