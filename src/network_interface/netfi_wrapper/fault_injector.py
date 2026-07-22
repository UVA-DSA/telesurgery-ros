import json
import os

import rclpy
from ament_index_python import get_package_share_directory
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from netfi.emulators import DelayEmulator, PacketLossEmulator, PacketReorderEmulator


class FaultInjector(Node):

    def __init__(self):
        super().__init__('fault_injector')
        self.declare_parameter('enable_fault_injector', False)
        self.declare_parameter('fault_injector_in_topic', 'netfi_in')
        self.declare_parameter('fault_injector_out_topic', 'netfi_out')

        self.enabled = self.get_parameter('enable_fault_injector').get_parameter_value().bool_value
        self.topic_in = self.get_parameter('fault_injector_in_topic').get_parameter_value().string_value
        self.topic_out = self.get_parameter('fault_injector_out_topic').get_parameter_value().string_value

        package_share_dir = get_package_share_directory('network_interface')
        self.json_path = os.path.join(package_share_dir, 'netfi_config')

        self.delay = None
        self.loss = None
        self.reorder = None

    def load_json(self, filename):
        with open(os.path.join(self.json_path, filename), 'r') as f:
            return json.load(f)

    def start_delay(self):
        self.get_logger().info("Starting delay fault injector")
        params = self.load_json("delay_config.json")

        self.delay = DelayEmulator(input_port=0, output_port=0, network_type='5G',
                                   params=params, protocol='ros2',
                                   node=self, input_topic=self.topic_in, output_topic=self.topic_out, msg_type_str='teleop_msgs/ITP')
        self.delay.start()

    def start_loss(self):
        self.get_logger().info("Starting loss fault injector")
        params = self.load_json("packet_loss_config.json")
        self.loss = PacketLossEmulator(input_port=0, output_port=0,
                                             model_name='Communication_Loss',
                                             params=params, protocol='ros2',
                                       node=self, input_topic=self.topic_in, output_topic=self.topic_out, msg_type_str='teleop_msgs/ITP')
        self.loss.start()

    def start_reorder(self):
        self.get_logger().info("Starting reorder fault injector")
        params = self.load_json("packet_reorder_config.json")
        self.reorder = PacketReorderEmulator(input_port=0, output_port=0,
                                          params = params, protocol='ros2',
                                          node=self, input_topic=self.topic_in, output_topic=self.topic_out, msg_type_str='teleop_msgs/ITP')
        self.reorder.start()


def main(args=None):
    try:
        with rclpy.init(args=args):
            node = FaultInjector()

            if node.enabled:
                node.start_reorder()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()