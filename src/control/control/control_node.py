import rclpy
from rclpy import Node
from rclpy.executors import ExternalShutdownException

### todo the kinematic controller, but it's currently bundled with surrol and I don't know where it is yet, so unimplemented
class Control(Node):
    def __init__(self):
        super().__init__('control_node')


def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            input_node = Control()

            rclpy.spin(input_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
