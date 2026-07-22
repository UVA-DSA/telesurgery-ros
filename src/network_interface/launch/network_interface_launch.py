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
    config_arg = DeclareLaunchArgument(
        'config',
        default_value='ros',
        description='Select config file (without the .yaml)'
    )
    
    enable_fault_injector_arg = DeclareLaunchArgument(
        'enable_fault_injector',
        default_value='true',
        description='Enable fault injector for network_interface node'
    )

    config_file_path = PathJoinSubstitution([
        FindPackageShare('network_interface'),
        'param',
        [LaunchConfiguration('config'), '.yaml']
    ])

    return LaunchDescription([
        config_arg,
        enable_fault_injector_arg,
        Node(
            package='network_interface',
            executable='network_interface',
            name='network_interface',
            parameters=[
                config_file_path,
                {'enable_fault_injector': LaunchConfiguration('enable_fault_injector')}
            ]
        ),
        Node(
            package='network_interface',
            executable='netfi_wrapper',
            name='netfi_wrapper',
            parameters=[
                config_file_path,
                {'enable_fault_injector': LaunchConfiguration('enable_fault_injector')}
            ]
        )
    ])