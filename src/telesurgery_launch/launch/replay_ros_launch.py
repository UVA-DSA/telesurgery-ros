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
                    file_path="launch/console_replay_launch.py"
                )
            ),
            launch_arguments={
                'config': 'ros'
            }.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_share_file(
                    package_name="network_interface",
                    file_path="launch/network_interface_launch.py"
                )
            ),
            launch_arguments={
                'config': 'ros'
            }.items(),
        ),

        Node(
            package='surrol_wrapper',
            executable='surrol_wrapper',
            name='surrol_wrapper',
            arguments=[]
        ),
    ])