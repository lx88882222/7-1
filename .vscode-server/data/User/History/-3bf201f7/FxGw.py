'''
提供一个move固定时间的函数move_t_sec(t,mode,speed)，其中mode=0:直行,mode=1:横向,mode=2:旋转.最大纵向速度1.6，最大横移速度0.55， 最大角速度2.5.
注意必须输入浮点数
0519
lx
照着rotate试图重构了一版，稳定性有所提高，但是bug依然存在，连续运行两次move_t_sec()可能会导致第二次无法运行，原因未知。有时第一个move运行失败，但第二次正常。😔唉
'''
import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import rclpy
import threading
import time

class MoveNode(Node):
    def __init__(self, name, mode, speed, duration):
        super().__init__(name)
        self.motion_id = 305
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        if mode == 0:
            self.speed_x = speed
        elif mode == 1:
            self.speed_y = speed
        elif mode == 2:
            self.speed_z = speed
            self.motion_id = 303
        self.dog_name = "az"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.duration = duration
        self.elapsed_time=-0.1
        self.time_enough = False
        print(f'start at {time.time()}')

    def timer_callback(self):
        self.elapsed_time += 0.1
        if self.elapsed_time < self.duration:#还没走够时间
            msg = MotionServoCmd()
            msg.motion_id = self.motion_id
            msg.cmd_type = 1
            msg.value = 2
            msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
            msg.step_height = [0.05, 0.05]
            self.pub.publish(msg)
            print(f'go at {time.time()}')
        else:
            # 走够了，停下
            self.time_enough = True
            msg = MotionServoCmd()
            msg.motion_id = self.motion_id
            msg.cmd_type = 1
            msg.value = 2
            msg.vel_des = [0.0, 0.0, 0.0]
            msg.step_height = [0.05, 0.05]
            self.pub.publish(msg)
            print(f'stop at {time.time()}')
            self.time_enough = True

def move_t_sec(t, mode, speed):
    rclpy.init(args=None)
    move_node = MoveNode("move_node",mode,speed,t)
    move_thread = threading.Thread(target=rclpy.spin, args=(move_node,))
    move_thread.start()
    while not move_node.time_enough:
        pass
    move_node.destroy_node()
    rclpy.shutdown()
    return True
def main(args=None):
    move_t_sec(1.14597405796519, 0, 0.5)
    move_t_sec(1.14597405796519, 0, -0.5)


if __name__ == "__main__":
    main()