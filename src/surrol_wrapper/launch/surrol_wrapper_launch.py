import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params_arg = DeclareLaunchArgument(
        'config',
        default_value='new',
        description='PSelect config file (without the .yaml)'
    )

    config_file_path = PathJoinSubstitution([
        FindPackageShare('surrol_wrapper'),
        'param',
        [LaunchConfiguration('config'), '.yaml']
    ])

    surrol_node = Node(
        package='surrol_wrapper',
        executable='surrol_wrapper',
        name='surrol_node',
        output='screen',
        parameters=[config_file_path],
    )

    return LaunchDescription([
        params_arg,
        surrol_node,
    ])
