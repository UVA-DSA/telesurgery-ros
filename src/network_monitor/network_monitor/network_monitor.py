import random

import rclpy
from rcl_interfaces.srv import GetParameters
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from network_monitor.profiler import Profiler
from teleop_msgs.srv import NetworkStatistics


class NetworkMonitor(Node):
    def __init__(self):
        super().__init__('network_monitor')
        self.declare_parameter('profiler', False)

        self.create_service(NetworkStatistics, "/network_statistics", self.statistics_callback)

        self.profiler_enabled = self.get_parameter('profiler').get_parameter_value().bool_value

        self.profiler = None


    def statistics_callback(self, request, response: NetworkStatistics):
        rand_float = random.uniform(0, 1)
        response.interarrival_sd = rand_float
        return response


def main(args=None):
    try:
        with rclpy.init(args=args):
            node = NetworkMonitor()

            node.get_logger().info("Starting dummy network monitor. This hosts a service that returns network statistics on request.")

            if node.profiler_enabled:
                node.get_logger().info("Starting profiler.")
                node.profiler = Profiler(node)

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
