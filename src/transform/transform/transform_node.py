import rclpy
from rclpy import Node
from rclpy.executors import ExternalShutdownException

from teleop_msgs import ITP

class Transform(Node):
    def __init__(self):
        super().__init__('transform')
        self.ITP_sub = self.create_subscription(
            ITP,
            '/itp_comamnds',
            self.ITP_callback,
            10)

    def ITP_callback(self, msg: ITP):
        pass


def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = Transform()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
