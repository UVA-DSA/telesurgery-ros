import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def get_share_file(package_name, file_path):
    return os.path.join(get_package_share_directory(package_name), file_path)

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='console_replay',
            executable='console_replay',
            name='console_replay',
            parameters=[get_share_file("console_replay", "param/udp.yaml")]
        ),
    ])