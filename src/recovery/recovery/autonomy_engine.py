import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

class AutonomyEngine(Node):
    def __init__(self):
        super().__init__('autonomy_engine')


def main(args=None):
    try:
        with rclpy.init(args=args):
            node = AutonomyEngine()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
