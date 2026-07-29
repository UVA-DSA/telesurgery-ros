import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def get_share_file(package_name, file_path):
    return os.path.join(get_package_share_directory(package_name), file_path)

def generate_launch_description():
    enable_fault_injector_arg = DeclareLaunchArgument(
        'enable_fault_injector',
        default_value='False',
        description='Enable fault injector'
    )

    enable_fault_injector = LaunchConfiguration('enable_fault_injector')

    return LaunchDescription([
        enable_fault_injector_arg,
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
                'config': 'ros',
                'enable_fault_injector': enable_fault_injector
            }.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_share_file(
                    package_name="surrol_wrapper",
                    file_path="launch/surrol_wrapper_launch.py"
                )
            ),
            launch_arguments={
                'config': 'final',
            }.items()
        ),

        Node(
            package='recovery',
            executable='fault_recovery_state_machine',
            name='fault_recovery_state_machine',
            arguments=[]
        ),

        Node(
            package='recovery',
            executable='autonomy_engine',
            name='autonomy_engine',
            arguments=[]
        ),

        Node(
            package='command_switch',
            executable='command_switch',
            name='command_switch',
            arguments=[]
        )
    ])