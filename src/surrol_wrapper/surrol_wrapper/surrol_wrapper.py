import threading

import rclpy
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node

from . import multiple_scenes_console_replay


class Surrol(Node):
    def __init__(self):
        super().__init__('surrol_node')

    def run_sim(self):
        multiple_scenes_console_replay.main(node=self)

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