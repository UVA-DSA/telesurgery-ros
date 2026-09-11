import os
import threading

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from std_msgs.msg import Bool
from rcl_interfaces.msg import ParameterDescriptor

from teleop_msgs.msg import ITP
from .replay import Replay


class ConsoleReplay(Node):

    def __init__(self):
        super().__init__('console_replay')
        package_share_dir = get_package_share_directory('console_replay')

        self.init_parameters()

        data_file_path = os.path.join(
            package_share_dir,
            'replay_files',
            self.get_parameter('data_file_name').get_parameter_value().string_value
        )

        if not os.path.isfile(data_file_path):
            raise FileNotFoundError(f"Replay file {data_file_path} not found")

        self.replay_obj = Replay(filepath=data_file_path, node=self)

        self.subscription = self.create_subscription(
            Bool,
            'replay_start',
            self.start,
            10
        )
        self.thread: threading.Thread = None

        self.itp_publisher = self.create_publisher(ITP,
                                self.get_parameter('ros_topic_name').get_parameter_value().string_value,
                                100)

    def init_parameters(self):
        data_file_path_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='File name of replay data - must be in in replay_files directory'
        )
        self.declare_parameter('data_file_name', '', descriptor=data_file_path_descriptor)

        ros_topic_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='ROS topic name'
        )
        self.declare_parameter('ros_topic_name', '/agent/itp_commands', descriptor=ros_topic_descriptor)


    def start(self, msg: Bool):
        # Wait for a message to be sent to the /replay_start topic
        if not msg.data: return

        if self.thread:
            self.get_logger().info("(re)-Starting replay!")
            self.thread.join()
        else:
            self.get_logger().info("Starting replay!")

        self.thread = threading.Thread(
            target=self.replay_obj.replay_ros,
            args=(self.itp_publisher,)
        )
        self.thread.start()

def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            replay_node = ConsoleReplay()

            rclpy.spin(replay_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
