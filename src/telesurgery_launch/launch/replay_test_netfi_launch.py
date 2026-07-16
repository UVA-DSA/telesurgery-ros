import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def get_share_file(package_name, file_path):
    return os.path.join(get_package_share_directory(package_name), file_path)

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_share_file(
                    package_name="console_replay",
                    file_path="launch/console_replay_launch_udp_netfi.py"
                )
            )
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_share_file(
                    package_name="netfi_wrapper",
                    file_path="launch/netfi_launch_test_delay.py"
                )
            )
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_share_file(
                    package_name="network_interface",
                    file_path="launch/network_interface_launch_udp.py"
                )
            )
        ),

        Node(
            package='surrol_wrapper',
            executable='surrol_wrapper',
            name='surrol_wrapper',
            arguments=[]
        ),
    ])