import rclpy
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from network_interface.data_flow import DataFlow
from network_interface.fault_injector import FaultInjector


class NetworkInterface(Node):

    def __init__(self):
        super().__init__('network_interface')

        self.init_parameters()

        self.data_flow = DataFlow(self)
        self.fault_injector = FaultInjector(self)

    def init_parameters(self):
        ### DATA FLOW

        input_mode_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='Mode of listening to input: either ROS or UDP'
        )
        self.declare_parameter('data_flow.input_mode', '', input_mode_descriptor)

        ros_topic_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='ROS topic name to listen to'
        )
        self.declare_parameter('data_flow.listen_topic_name', '/itp_commands_raw', descriptor=ros_topic_descriptor)

        ros_topic_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='ROS topic name to publish to'
        )
        self.declare_parameter('data_flow.publish_topic_name', '/itp_commands', descriptor=ros_topic_descriptor)

        udp_ip_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='UDP IP address to set up a server on'
        )
        self.declare_parameter('data_flow.udp_ip', '127.0.0.1', descriptor=udp_ip_descriptor)

        udp_port_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.INTEGER,
            description='UDP port number to set up a server on'
        )
        self.declare_parameter('data_flow.udp_port', 5001, descriptor=udp_port_descriptor)

        ### FAULT INJECTOR

        data_file_path_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.INTEGER,
            description='Port to listen on for fault injection'
        )
        self.declare_parameter('fault_injector.emulator_port', 36000, descriptor=data_file_path_descriptor)

        data_file_path_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.INTEGER,
            description='Port to send to for fault injection'
        )
        self.declare_parameter('fault_injector.receiver_port', 5001, descriptor=data_file_path_descriptor)


def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = NetworkInterface()

            node.fault_injector.delay.start()

            mode = node.get_parameter('data_flow.input_mode').get_parameter_value().string_value.lower()
            if mode == 'ros':
                node.data_flow.init_ros_listener()
            elif mode == 'udp':
                node.data_flow.init_sock_udp()
                node.data_flow.listen_thread.start()
            else:
                raise KeyError(f"Unsupported mode: {mode}")

            node.data_flow.publish_thread.start()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
