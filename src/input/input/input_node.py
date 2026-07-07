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
        self.udp_queue: Queue = queue.Queue()

        self.fields = 'sequence pactyp version delx0 delx1 dely0 dely1 delz0 delz1 Qx0 Qx1 Qy0 Qy1 Qz0 Qz1 Qw0 Qw1 buttonstate0 buttonstate1 grasp0 grasp1 surgeon_mode checksum'.split()
        self.UStruct = namedtuple('UStruct', self.fields)
        self.format_str = '<IIIiiiiiiddddddddiiiiii'

        self.init_sock_udp()
        self.publish_thread = threading.Thread(target=self.publish_itp, daemon=True)
        self.publish_thread.start()
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
                unpacked_data = struct.unpack(self.format_str, data)
                u_struct = self.UStruct(*unpacked_data)
                command = u_struct._asdict()
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

    def publish_itp(self):
        while True:
            if self.udp_queue.empty(): continue
            msg = self.to_msg(self.udp_queue.get())
            self.itp_publisher.publish(msg)
            self.get_logger().info("published ITP message")


    def to_msg(self, d) -> ITP:
        msg: ITP = ITP()
        msg.sequence = d['sequence']
        msg.pactyp = d['pactyp']
        msg.version = d['version']
        msg.delx0 = d['delx0']
        msg.delx1 = d['delx1']
        msg.dely0 = d['dely0']
        msg.dely1 = d['dely1']
        msg.delz0 = d['delz0']
        msg.delz1 = d['delz1']
        msg.qx0 = d['Qx0']
        msg.qx1 = d['Qx1']
        msg.qy0 = d['Qy0']
        msg.qy1 = d['Qy1']
        msg.qz0 = d['Qz0']
        msg.qz1 = d['Qz1']
        msg.qw0 = d['Qw0']
        msg.qw1 = d['Qw1']
        msg.buttonstate0 = d['buttonstate0']
        msg.buttonstate1 = d['buttonstate1']
        msg.grasp0 = d['grasp0']
        msg.grasp1 = d['grasp1']
        msg.surgeon_mode = d['surgeon_mode']
        msg.checksum = d['checksum']
        return msg



def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            input_node = Input()

            rclpy.spin(input_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
