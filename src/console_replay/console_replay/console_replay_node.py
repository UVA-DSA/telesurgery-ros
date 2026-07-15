import os

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from std_msgs.msg import Bool
from rcl_interfaces.msg import ParameterDescriptor

from teleop_msgs.msg import ITPRaw
from .replay import replayoverport


## This node wraps replay.py from the telesurgery-qos-analysis repository.
## It sends packets over UDP, not over ROS2.
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

        self.replay_obj = replayoverport(filepath=data_file_path)

        self.subscription = self.create_subscription(
            Bool,
            'replay_start',
            self.start,
            10
        )

        self.itp_raw_publisher = self.create_publisher(ITPRaw, 'itp_commands_raw', 100)

    def init_parameters(self):
        data_file_path_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='File name of replay data - must be in in replay_files directory'
        )
        self.declare_parameter('data_file_name', '', descriptor=data_file_path_descriptor)

        output_mode_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='Whether to output UDP packets (UDP) or ROS2 messages (ROS)'
        )
        self.declare_parameter('output_mode', 'ROS', descriptor=output_mode_descriptor)

        ros_topic_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='ROS topic name'
        )
        self.declare_parameter('ros_topic_name', '/itp_commands', descriptor=ros_topic_descriptor)

        udp_ip_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='UDP IP address'
        )
        self.declare_parameter('udp_ip', '127.0.0.1', descriptor=udp_ip_descriptor)

        udp_port_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.INTEGER,
            description='UDP port number'
        )
        self.declare_parameter('udp_port', 5001, descriptor=udp_port_descriptor)


    def start(self, msg: Bool):
        if not msg.data: return
        mode = self.get_parameter('output_mode').get_parameter_value().string_value
        if mode.lower() == 'udp':
            self.get_logger().info("Starting replay on UDP")
            self.replay_obj.replay_log(dest_ip=self.get_parameter('udp_ip').get_parameter_value().string_value,
                                       dest_port=self.get_parameter('udp_port').get_parameter_value().integer_value)
        elif mode.lower() == 'ros' or mode.lower() == 'ros2':
            self.get_logger().info("Starting replay on ROS")
            self.replay_obj.replay(self.itp_raw_publisher)
        else:
            raise KeyError(f"Unsupported mode: {mode}")

def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            replay_node = ConsoleReplay()

            rclpy.spin(replay_node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
