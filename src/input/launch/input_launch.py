import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def get_share_file(package_name, file_path):
    return os.path.join(get_package_share_directory(package_name), file_path)

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='input',
            executable='input',
            name='input',
            parameters=[get_share_file("input", "param/default.yaml")]
        ),
    ])