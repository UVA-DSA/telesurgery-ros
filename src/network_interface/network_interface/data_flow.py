import queue
import socket
import threading
from queue import Queue

import rclpy
from teleop_msgs.msg import ITPRaw, ITP
from teleop_msgs_helpers import ITP_helpers


class DataFlow:
    def __init__(self, node: rclpy.node.Node):
        self.node: rclpy.Node = node

        self.itp_publisher = self.node.create_publisher(ITP, '/itp_commands', 100)
        self.subscription = None
        self.sock = None
        self.ip = self.node.get_parameter('data_flow.udp_ip').get_parameter_value().string_value
        self.port = self.node.get_parameter('data_flow.udp_port').get_parameter_value().integer_value
        self.udp_queue: Queue = queue.Queue()

        self.publish_thread = threading.Thread(target=self.publish_itp, daemon=True)
        self.listen_thread = threading.Thread(target=self.udp_listener, daemon=True)


    def init_sock_udp(self):
        # Create a UDP socket and the data struct ----------------------------------------------------
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)
        self.sock.bind((self.ip, self.port))
        self.node.get_logger().info(f"Initialized a UDP server on IP: {self.ip} and port: {self.port}")
        self.node.get_logger().info("Listening for incoming data:")

    def init_ros_listener(self):
        self.subscription = self.node.create_subscription(
            ITPRaw,
            self.node.get_parameter('data_flow.listen_topic_name').get_parameter_value().string_value,
            self.itp_raw_callback,
            100
        )

    def itp_raw_callback(self, msg: ITPRaw):
        command = ITP_helpers.raw_to_dict(msg)
        self.udp_queue.put(command)

    def udp_listener(self):
        # Taken from Console.py
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)  # Buffer size of 1024 bytes
                command = ITP_helpers.bytes_to_dict(data)
                self.udp_queue.put(command)

            except socket.timeout:
                # Timeout reached, continue listening
                continue
            except Exception as e:
                self.node.get_logger().error(f"Error receiving packet: {e}")
                # self.get_logger().error(traceback.format_exc())

    def publish_itp(self):
        while True:
            command = self.udp_queue.get()
            msg = ITP_helpers.to_msg(command)
            self.itp_publisher.publish(msg)