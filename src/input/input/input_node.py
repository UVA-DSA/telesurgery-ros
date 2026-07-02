import os
import socket

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from teleop_msgs.msg import ITP

## Converts raw packets into ITP ROS messages
## Currently assumes that the raw packets are coming in through UDP.
## I am not sure if this should instead accept a ROS message representation of the packets
class Input(Node):

    def __init__(self):
        super().__init__('input')

        self.itp_publisher = self.create_publisher(ITP, '/itp_commands', 10)
        self.sock = None
        self.ip = '127.0.0.1'
        self.port = 5001

        self.init_sock_udp()
        self.udp_listener()

    def init_sock_udp(self):
        # Create a UDP socket and the data struct ----------------------------------------------------
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)
        self.sock.bind((self.ip, self.port))
        self.get_logger().info(f"Initialized a UDP server on IP: {self.ip} and port: {self.port}")
        self.get_logger().info("Listening for incoming data:")

    def udp_listener(self):
        # Taken from Console.py
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)  # Buffer size of 1024 bytes
                self.publish_itp()
                # u_struct = self.unpack_data(data)
                # command = u_struct._asdict()
                # self.udp_queue.put(command)

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

    def publish_itp(self):
        msg = ITP()
        msg.sequence = 42
        self.itp_publisher.publish(msg)
        self.get_logger().info("Published dummy ITP message to /itp_commands")



def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            input_node = Input()

            rclpy.spin(input_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
