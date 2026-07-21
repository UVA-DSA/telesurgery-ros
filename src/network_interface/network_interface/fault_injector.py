import rclpy
from netfi.emulators import DelayEmulator


class FaultInjector:

    def __init__(self, node: rclpy.node.Node):
        self.node: rclpy.Node = node

        self.enabled = node.get_parameter('fault_injector.enabled').get_parameter_value().bool_value

        self.emulator_port = self.node.get_parameter('fault_injector.emulator_port').get_parameter_value().integer_value
        self.receiver_port = self.node.get_parameter('fault_injector.receiver_port').get_parameter_value().integer_value

        self.delay = None

    def start_delay(self):
        # For now, let's run the delay emulator just to verify it works
        delay_params = {
            'lower_bound': 7.5,
            'weights': [0.8, 0.2],
            'lambdas': [0.2, 0.02],
        }
        actual_params = {
            '5G': delay_params
        }

        self.delay = DelayEmulator(input_port=self.emulator_port, output_port=self.receiver_port, network_type='5G',
                                   params=actual_params, protocol='ros2',
                                   node=self.node, input_topic='netfi_in', output_topic='netfi_out', msg_type_str='teleop_msgs/ITPRaw')
        self.delay.start()