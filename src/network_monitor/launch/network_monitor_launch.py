import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def get_share_file(package_name, file_path):
    return os.path.join(get_package_share_directory(package_name), file_path)

def generate_launch_description():
    profiler_arg = DeclareLaunchArgument(
        'profiler',
        default_value='False',
        description='Enable profiler'
    )

    return LaunchDescription([
        profiler_arg,
        Node(
            package='network_monitor',
            executable='network_monitor',
            name='network_monitor',
            parameters=[
                {'profiler': LaunchConfiguration('profiler')}
            ]
        ),
    ])