'''
> safe.py
> author: whf
> date: 2024-05-18
> paralleled obstacle-avoidance node
    subscribe: '/{dog_name}/phase' (String)

'''
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd
from std_msgs.msg import String
import time
import threading
from .sensor_node import sensor_suber

class safe_node(Node):
    def __init__(self, name):
        super().__init__(name)
        self.sensor_node = sensor_suber('sensor')
        self.speed_x, self.speed_y, self.speed_z = 0.1, 0.0, 0.0
        self.dog_name = "az1"
        self.cmd_pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.phase_pub = self.create_publisher(String,f'{self.dog_name}/phase',1)
        self.phase_pub = self.create_subscription(String,f'{self.dog_name}/phase',self.silent(),1)
        self.timer = None
        self.do_avoid = threading.Event()
        self.do_avoid.set()
        self.safe_thread = threading.Thread(target = self.safe(),args = (self), name = 'safe')
        self.cam_thread = threading.Thread(target=rclpy.spin, args=(self.sensor_node,),name = 'sensor_thread')
        self.safe_thread.start()
        self.cam_thread.start()

        # self.count +=1
        # self.get_logger().info(f"the distance is {self.count}")
    
    def silent(self,status:String):
        if (status.data == "make goal"):
            self.do_avoid.clear()
        else:
            self.do_avoid.set()
    def safe(self):
        while True:
            self.do_avoid.wait()
            self.get_logger().info("执行avoid")
            self.avoid()

    def avoid(self):
        if self.sensor_node.dist is not None and self.sensor_node.dist < 0.9:
            # 如果距离小于90cm，则开转
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.5
            self.get_logger().info(f"距离小于90cm，the distance is {self.sensor_node.dist}")
        if self.sensor_node.dist is not None and self.sensor_node.dist >= 0.9:
            # 如果距离大于90cm，则走
            self.speed_x, self.speed_y, self.speed_z = 0.3, 0.0, 0.0
            self.get_logger().info(f"距离大于90，the distance is {self.sensor_node.dist}")
        msg = MotionServoCmd()
        msg.motion_id = 308
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05,0.05]
        self.cmd_pub.publish(msg)
        self.get_logger().info(f"the distance is {self.sensor_node.dist}")
        time.sleep(0.1)