import rclpy
from rclpy.node import Node
from protocol.srv import MotionResultCmd

class basic_cmd(Node):
    def __init__(self, name):
        super().__init__(name)
        self.client = self.create_client(MotionResultCmd, '/az1/motion_result_cmd')
        # while not self.client.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        self.request = MotionResultCmd.Request()

    def send_request(self):
        self.request.motion_id = 132
        self.future = self.client.call_async(self.request)

def main(args=None):
        rclpy.init(args=args)
        movenode = basic_cmd("basic_cmd")
        movenode.send_request()
        while rclpy.ok():
            rclpy.spin_once(movenode)
            if movenode.future.done():
                try:
                    response = movenode.future.result()
                except Exception as e:
                    movenode.get_logger().info('Service call failed %r'%(e,))
            else:
                movenode.get_logger().info("cmd has done!")
            break
        movenode.destroy_node() 
        rclpy.shutdown()
