import rclpy
from rclpy import Future
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from teleop_msgs.msg import RecoveryStatus
from teleop_msgs.srv import NetworkStatistics


class FaultRecoveryStateMachine(Node):
    def __init__(self):
        super().__init__('fault_recovery_state_machine')
        self.publisher_ = self.create_publisher(RecoveryStatus, '/recovery_type', 10)
        self.client = self.create_client(NetworkStatistics, '/network_statistics')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for /network_statistics service")
        self.timer = self.create_timer(10, self.dummy_timer_callback)
        self.state = RecoveryStatus.NORMAL_OPERATION

    def dummy_timer_callback(self):
        future = self.fetch_network_statistics()
        future.add_done_callback(self.service_callback)

    def fetch_network_statistics(self) -> Future:
        return self.client.call_async(NetworkStatistics.Request())

    def service_callback(self, future):
        response = future.result()
        self.get_logger().info(f"Random double from network monitor was {response}")
        msg = RecoveryStatus()
        msg.state = self.state
        self.publisher_.publish(msg)
        if self.state == RecoveryStatus.NORMAL_OPERATION:
            self.state = RecoveryStatus.LONG_TERM_RECOVERY
        else:
            self.state = RecoveryStatus.NORMAL_OPERATION

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = FaultRecoveryStateMachine()

            node.get_logger().info("Starting dummy fault recovery state machine. "
                                   "This alternates between normal operation and long-term recovery every 10s,"
                                   "and publishes the state to /recovery_type")

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
