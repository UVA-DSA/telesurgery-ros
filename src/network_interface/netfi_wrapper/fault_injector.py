import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from netfi.emulators import DelayEmulator


class FaultInjector(Node):

    def __init__(self):
        super().__init__('fault_injector')
        self.declare_parameter('enable_fault_injector', False)
        self.declare_parameter('fault_injector_in_topic', 'netfi_in')
        self.declare_parameter('fault_injector_out_topic', 'netfi_out')

        self.enabled = self.get_parameter('enable_fault_injector').get_parameter_value().bool_value
        self.topic_in = self.get_parameter('fault_injector_in_topic').get_parameter_value().string_value
        self.topic_out = self.get_parameter('fault_injector_out_topic').get_parameter_value().string_value

        self.delay = None

    def start_delay(self):
        self.get_logger().info("Starting delay fault injector")
        # For now, let's run the delay emulator just to verify it works
        delay_params = {
            'lower_bound': 7.5,
            'weights': [0.8, 0.2],
            'lambdas': [0.2, 0.02],
        }
        actual_params = {
            '5G': delay_params
        }

        self.delay = DelayEmulator(input_port=0, output_port=0, network_type='5G',
                                   params=actual_params, protocol='ros2',
                                   node=self, input_topic=self.topic_in, output_topic=self.topic_out, msg_type_str='teleop_msgs/ITP')
        self.delay.start()


def main(args=None):
    try:
        with rclpy.init(args=args):
            node = FaultInjector()

            if node.enabled:
                node.start_delay()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()