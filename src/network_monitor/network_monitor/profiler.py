import time

import rclpy
from std_msgs.msg import Int32, Float32

from teleop_msgs.msg import ITP


class Profiler:
    def __init__(self, node):
        self.node: rclpy.node.Node = node
        self.sequences: dict = {}

        self.first_received_sub = self.node.create_subscription(Int32, '/profiler/first_received', self.first_received_callback, 10)
        self.simulator_sub = self.node.create_subscription(ITP, '/final/itp_commands', self.simulator_input_callback, 10)
        self.latency_pub = self.node.create_publisher(Int32, '/profiler/latency', 10)


    def first_received_callback(self, msg: Int32):
        self.sequences[msg.data] = time.time_ns()

    def simulator_input_callback(self, msg: ITP):
        out = Int32()
        t = self.sequences.get(msg.sequence, None)
        if t is not None:
            self.node.get_logger().info(f"begin: {t} end: {time.time_ns()}")
            out.data = (time.time_ns() - t) // 1000000
            self.latency_pub.publish(out)
            del self.sequences[msg.sequence]