import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from . import multiple_scenes_console_replay


class Surrol(Node):
    def __init__(self):
        super().__init__('surrol_node')

        multiple_scenes_console_replay.main(node=self)

def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = Surrol()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()