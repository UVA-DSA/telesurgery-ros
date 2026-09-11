import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def get_share_file(package_name, file_path):
    return os.path.join(get_package_share_directory(package_name), file_path)

def generate_launch_description():
    config_arg = DeclareLaunchArgument(
        'config',
        default_value='ros',
        description='Select config file (without the .yaml)'
    )

    config_file_path = PathJoinSubstitution([
        FindPackageShare('console_replay'),
        'param',
        [LaunchConfiguration('config'), '.yaml']
    ])

    return LaunchDescription([
        config_arg,
        Node(
            package='console_replay',
            executable='console_replay',
            name='console_replay',
            parameters=[config_file_path]
        ),
    ])