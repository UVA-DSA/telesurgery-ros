from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='console_replay',
            executable='console_replay',
            name='console_replay_node',
            # todo this is for something important, don't know what yet
            arguments=[]
        ),

        Node(
            package='input',
            executable='input',
            name='input_node',
            arguments=[]
        ),

        Node(
            package='surrol_wrapper',
            executable='surrol_wrapper',
            name='surrol_wrapper',
            arguments=[]
        ),
    ])