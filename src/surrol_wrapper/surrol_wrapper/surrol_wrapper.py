import threading

import rclpy
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node

from . import multiple_scenes_console_replay


class Surrol(Node):
    def __init__(self):
        super().__init__('surrol_node')
        self.init_parameters()

    def run_sim(self):
        multiple_scenes_console_replay.main(node=self)

    def init_parameters(self):
        topic_name_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='Topic to listen to'
        )
        self.declare_parameter('simulator_input_topic', '/final/itp_commands', descriptor=topic_name_descriptor)

def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = Surrol()

            ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
            ros_thread.start()

            multiple_scenes_console_replay.main(node=node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()