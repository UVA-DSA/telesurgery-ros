import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node

def get_share_file(package_name, file_path):
    return os.path.join(get_package_share_directory(package_name), file_path)

def generate_launch_description():
    enable_fault_injector_arg = DeclareLaunchArgument(
        'enable_fault_injector',
        default_value='False',
        description='Enable fault injector'
    )

    enable_recovery_arg = DeclareLaunchArgument(
        'recovery',
        default_value='False',
        description='Enable recovery nodes'
    )

    enable_profiler_arg = DeclareLaunchArgument(
        'profiler',
        default_value='False',
        description='Enable profiler'
    )

    enable_logger_arg = DeclareLaunchArgument(
        'logger',
        default_value='False',
        description='Enable logger'
    )

    enable_fault_injector = LaunchConfiguration('enable_fault_injector')
    enable_recovery = LaunchConfiguration('recovery')
    enable_profiler = LaunchConfiguration('profiler')
    enable_logger = LaunchConfiguration('logger')

    return LaunchDescription([
        enable_fault_injector_arg,
        enable_recovery_arg,
        enable_profiler_arg,
        enable_logger_arg,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_share_file(
                    package_name="network_interface",
                    file_path="launch/network_interface_launch.py"
                )
            ),
            launch_arguments={
                'config': 'udp',
                'enable_fault_injector': enable_fault_injector,
                'profiler': enable_profiler,
                'logger': enable_logger
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

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_share_file(
                    package_name="recovery",
                    file_path="launch/recovery_launch.py"
                )
            ),
            launch_arguments={
                'config': 'replay',
            }.items(),
            condition=IfCondition(enable_recovery)
        ),

        Node(
            package='master_controller',
            executable='master_controller',
            name='master_controller',
            arguments=[],
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_share_file(
                    package_name="network_monitor",
                    file_path="launch/network_monitor_launch.py"
                )
            ),
            launch_arguments={
                'profiler': enable_profiler
            }.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_share_file(
                    package_name="video",
                    file_path="launch/video_launch.py"
                )
            ),
            launch_arguments={
                'config': 'config',
            }.items(),
        )
    ])