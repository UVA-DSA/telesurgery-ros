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

            mode = node.get_parameter('data_flow.input_mode').get_parameter_value().string_value.lower()
            fault_injector_enabled = node.get_parameter('enable_fault_injector').get_parameter_value().bool_value
            logger_enabled = node.get_parameter('enable_logger').get_parameter_value().bool_value
            node.get_logger().info(f"Starting in {mode} mode")

            if logger_enabled:
                node.get_logger().info("Packet Writer Logger starting")
                node.data_flow.logger = PacketWriter()
                node.data_flow.logger.packet_writer_thread.start()
            if mode == 'ros':
                pass
            elif mode == 'udp':
                node.data_flow.init_sock_udp()
                node.data_flow.listen_thread.start()
            else:
                raise KeyError(f"Unsupported mode: {mode}")

            if fault_injector_enabled:
                node.data_flow.publish_fault_injector_thread.start()

            node.data_flow.publish_thread.start()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
