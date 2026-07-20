import rclpy
from netfi.emulators import PacketLossEmulator, DelayEmulator
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class FaultInjector:

    def __init__(self, node: rclpy.Node):
        self.node: rclpy.Node = node

        self.emulator_port = self.node.get_parameter('fault_injector.emulator_port').get_parameter_value().integer_value
        self.receiver_port = self.node.get_parameter('fault_injector.receiver_port').get_parameter_value().integer_value

        # For now, let's run the delay emulator just to verify it works
        delay_params = {
            'lower_bound': 7.5,
            'weights': [0.8, 0.2],
            'lambdas': [0.2, 0.02],
        }
        actual_params = {
            '5G': delay_params
        }

        self.delay = DelayEmulator(input_port=self.emulator_port, output_port=self.receiver_port, network_type='4G',
                                   params=actual_params, protocol='udp')