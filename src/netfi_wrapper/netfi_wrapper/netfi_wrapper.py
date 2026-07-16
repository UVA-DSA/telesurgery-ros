import rclpy
from netfi.emulators import PacketLossEmulator, DelayEmulator
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class NetFIWrapper(Node):

    def __init__(self):
        super().__init__('netfi_wrapper')

        self.init_parameters()

        self.emulator_port = self.get_parameter('emulator_port').get_parameter_value().integer_value
        self.receiver_port = self.get_parameter('receiver_port').get_parameter_value().integer_value

        # For now, let's run the delay emulator just to verify it works
        delay_params = {
            'lower_bound': 15,
            'weights': [0.8, 0.2],
            'lambdas': [0.1, 0.0067],
        }
        actual_params = {
            '4G': delay_params
        }

        self.delay = DelayEmulator(input_port=self.emulator_port, output_port=self.receiver_port, network_type='4G',
                                   params=actual_params, protocol='udp')

    def init_parameters(self):
        data_file_path_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.INTEGER,
            description='Port to listen on'
        )
        self.declare_parameter('emulator_port', 36000, descriptor=data_file_path_descriptor)

        data_file_path_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.INTEGER,
            description='Port to send to'
        )
        self.declare_parameter('receiver_port', 5001, descriptor=data_file_path_descriptor)




def main(args=None):
    try:
        with rclpy.init(args=args):
            node = NetFIWrapper()

            node.delay.start()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()