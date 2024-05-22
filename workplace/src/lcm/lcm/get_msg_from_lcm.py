
import sys
path_add = r'/home/mi/workplace/src/lcm/lcm'
sys.path.append(path_add)
path_add = r'/home/mi/Downloads/lcm/lcm-python'
print(sys.path)
sys.path.append(path_add)
import lcm
import teest
print('ok')
def my_handler(channel, data):
    msg = teest.localization_lcmt.decode(data)
    print("Received message on channel \"%s\"" % channel)
    print(f"vBody:{msg.vBody}")
def main():
    # 创建LCM对象
    lcm_obj = lcm.LCM()

    # 订阅通道并设置回调
    subscription = lcm_obj.subscribe("global_to_robot", my_handler)

    try:
        # 开始监听
        while True:
            lcm_obj.handle()
    except KeyboardInterrupt:
        pass

    # 取消订阅
    lcm_obj.unsubscribe(subscription)