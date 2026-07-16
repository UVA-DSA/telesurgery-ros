import os
import queue
import socket
import struct
import threading
from collections import namedtuple
from queue import Queue

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from teleop_msgs.msg import ITP
from teleop_msgs_helpers import ITP_helpers

## Converts raw packets into ITP ROS messages
## Currently assumes that the raw packets are coming in through UDP.
## I am not sure if this should instead accept a ROS message representation of the packets
class Input(Node):

    def __init__(self):
        super().__init__('input')

        self.itp_publisher = self.create_publisher(ITP, '/itp_commands', 100)
        self.sock = None
        self.ip = '127.0.0.1'
        self.port = 5001
        self.udp_queue: Queue = queue.Queue()

        self.fields = 'sequence pactyp version delx0 delx1 dely0 dely1 delz0 delz1 Qx0 Qx1 Qy0 Qy1 Qz0 Qz1 Qw0 Qw1 buttonstate0 buttonstate1 grasp0 grasp1 surgeon_mode checksum'.split()
        self.UStruct = namedtuple('UStruct', self.fields)
        self.format_str = '<IIIiiiiiiddddddddiiiiii'

        self.init_sock_udp()
        self.publish_thread = threading.Thread(target=self.publish_itp, daemon=True)
        self.publish_thread.start()

        self.listen_thread = threading.Thread(target=self.udp_listener, daemon=True)
        self.listen_thread.start()

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

            rclpy.spin(input_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
