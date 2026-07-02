import rclpy
from rclpy import Node
from rclpy.executors import ExternalShutdownException

class Transform(Node):
    def __init__(self):
        super().__init__('transform')


def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = Transform()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
