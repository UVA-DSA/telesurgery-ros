import os

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from std_msgs.msg import Bool

from .replay import replayoverport


## This node wraps replay.py from the telesurgery-qos-analysis repository.
## It sends packets over UDP, not over ROS2.
class ConsoleReplay(Node):

    def __init__(self):
        super().__init__('console_replay')
        package_share_dir = get_package_share_directory('console_replay')

        # todo hardcoded, need to add ros2 configuration files
        data_file_path = os.path.join(
            package_share_dir,
            'replay_files',
            'console_data_complete_7.bin'
        )

        self.replay_obj = replayoverport(filepath=data_file_path)

        self.subscription = self.create_subscription(
            Bool,
            'replay_start',
            self.start,
            10
        )

    def start(self, msg: Bool):
        if not msg.data: return
        self.get_logger().info("Starting replay")
        self.replay_obj.replay_log(dest_ip='127.0.0.1')

def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            replay_node = ConsoleReplay()

            rclpy.spin(replay_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
