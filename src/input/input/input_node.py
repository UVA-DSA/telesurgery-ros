import os
import queue
import socket
import struct
import threading
from collections import namedtuple
from queue import Queue

import rclpy
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from teleop_msgs.msg import ITP, ITPRaw
from teleop_msgs_helpers import ITP_helpers

class Input(Node):

    def __init__(self):
        super().__init__('input')

        self.init_parameters()

        self.itp_publisher = self.create_publisher(ITP, '/itp_commands', 100)
        self.subscription = None
        self.sock = None
        self.ip = self.get_parameter('udp_ip').get_parameter_value().string_value
        self.port = self.get_parameter('udp_port').get_parameter_value().integer_value
        self.udp_queue: Queue = queue.Queue()

        self.fields = 'sequence pactyp version delx0 delx1 dely0 dely1 delz0 delz1 Qx0 Qx1 Qy0 Qy1 Qz0 Qz1 Qw0 Qw1 buttonstate0 buttonstate1 grasp0 grasp1 surgeon_mode checksum'.split()
        self.UStruct = namedtuple('UStruct', self.fields)
        self.format_str = '<IIIiiiiiiddddddddiiiiii'

        self.publish_thread = threading.Thread(target=self.publish_itp, daemon=True)
        self.listen_thread = threading.Thread(target=self.udp_listener, daemon=True)

    def init_parameters(self):
        input_mode_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='Mode of listening to input: either ROS or UDP'
        )
        self.declare_parameter('input_mode', '', input_mode_descriptor)

        ros_topic_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='ROS topic name to listen to'
        )
        self.declare_parameter('listen_topic_name', '/itp_commands_raw', descriptor=ros_topic_descriptor)

        ros_topic_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='ROS topic name to publish to'
        )
        self.declare_parameter('publish_topic_name', '/itp_commands', descriptor=ros_topic_descriptor)

        # todo maybe make these parameters global so we can just read these from the console_replay node
        udp_ip_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='UDP IP address to set up a server on'
        )
        self.declare_parameter('udp_ip', '127.0.0.1', descriptor=udp_ip_descriptor)

        udp_port_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.INTEGER,
            description='UDP port number to set up a server on'
        )
        self.declare_parameter('udp_port', 5001, descriptor=udp_port_descriptor)

    def init_sock_udp(self):
        # Create a UDP socket and the data struct ----------------------------------------------------
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)
        self.sock.bind((self.ip, self.port))
        self.get_logger().info(f"Initialized a UDP server on IP: {self.ip} and port: {self.port}")
        self.get_logger().info("Listening for incoming data:")

    def init_ros_listener(self):
        self.subscription = self.create_subscription(
            ITPRaw,
            self.get_parameter('listen_topic_name').get_parameter_value().string_value,
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
            except OSError as e:
                if not self.running:
                    break  # Expected on shutdown
                self.get_logger().error(f"Error receiving packet: {e}")
                break
            except Exception as e:
                self.get_logger().error(f"Error receiving packet: {e}")
                # self.get_logger().error(traceback.format_exc())

    def publish_itp(self):
        while True:
            command = self.udp_queue.get()
            msg = ITP_helpers.to_msg(command)
            self.itp_publisher.publish(msg)



def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            input_node = Input()

            mode = input_node.get_parameter('input_mode').get_parameter_value().string_value.lower()
            if mode == 'ros':
                input_node.init_ros_listener()
            elif mode == 'udp':
                input_node.init_sock_udp()
                input_node.listen_thread.start()
            else:
                raise KeyError(f"Unsupported mode: {mode}")

            input_node.publish_thread.start()

            rclpy.spin(input_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
