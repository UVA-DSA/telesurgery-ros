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

        self.itp_publisher = self.create_publisher(ITP, '')
        self.sock = None
        self.ip = '127.0.0.1'
        self.port = '5001'
        self.running = True

    def init_sock_udp(self):
        # Create a UDP socket and the data struct ----------------------------------------------------
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)
        self.sock.bind((self.ip, self.port))
        print(f"Initialized a UDP server on IP: {self.ip} and port: {self.port}")
        print("Listening for incoming data: \n")

    def udp_listener(self):
        # Taken from Console.py
        while self.running:
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
                print(f"Error receiving packet: {e}")
                break
            except Exception as e:
                print(f"Error receiving packet: {e}")

    def publish_itp(self):
        pass



def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            input_node = Input()

            rclpy.spin(input_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
