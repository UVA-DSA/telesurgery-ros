import rclpy
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from network_interface.data_flow import DataFlow

from network_interface.packet_writer import PacketWriter


class NetworkInterface(Node):

    def __init__(self):
        super().__init__('network_interface')

        self.init_parameters()

        self.fault_injector_enabled = self.get_parameter('enable_fault_injector').get_parameter_value().bool_value
        self.logger_enabled = self.get_parameter('enable_logger').get_parameter_value().bool_value
        self.input_mode = self.get_parameter('data_flow.input_mode').get_parameter_value().string_value

        self.data_flow = DataFlow(self)

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

        self.declare_parameter('enable_fault_injector', False)
        self.declare_parameter('fault_injector_in_topic', 'netfi_in')
        self.declare_parameter('fault_injector_out_topic', 'netfi_out')

        ### LOGGER

        self.declare_parameter('enable_logger', False)


def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = NetworkInterface()

            if node.logger_enabled:
                node.get_logger().info("Packet Writer Logger initializing")
                node.data_flow.logger = PacketWriter(node)

            mode = node.input_mode.lower()
            node.get_logger().info(f"Starting in {mode} mode")

            if mode == 'ros':
                node.data_flow.init_ros_io()
            elif mode == 'udp':
                node.data_flow.init_udp_io()
            else:
                raise KeyError(f"Unsupported mode: {mode}")

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
