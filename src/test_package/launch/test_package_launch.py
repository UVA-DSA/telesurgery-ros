from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='test_package',
            executable='talker',
            name='minimal_publisher',
            # todo this is for something important, don't know what yet
            arguments=[]
        ),

        Node(
            package='test_package',
            executable='listener',
            name='minimal_subscriber',
            arguments=[]
        )
    ])