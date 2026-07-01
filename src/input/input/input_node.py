import os

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

## Converts raw packets into ITP ROS messages
## Currently assumes that the raw packets are coming in through UDP.
## I am not sure if this should instead accept a ROS message representation of the packets
class Input(Node):

    def __init__(self):
        super().__init__('input')



def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            input_node = Input()

            rclpy.spin(input_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
