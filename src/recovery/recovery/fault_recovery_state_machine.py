import rclpy
from rclpy import Future
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from teleop_msgs.msg import RecoveryStatus
from teleop_msgs.srv import NetworkStatistics

from rcl_interfaces.msg import ParameterDescriptor


class FaultRecoveryStateMachine(Node):
    def __init__(self):
        super().__init__('fault_recovery_state_machine')
        self.init_parameters()
        self.publisher_ = self.create_publisher(RecoveryStatus, '/recovery_type', 10)
        self.client = self.create_client(NetworkStatistics, '/network_statistics')
        self.timer = self.create_timer(10, self.dummy_timer_callback)
        self.state = RecoveryStatus.NORMAL_OPERATION

        # overrides
        self.override = self.get_parameter('state_machine.state_override').get_parameter_value().string_value

        if self.override == "AGENT":
            self.state = RecoveryStatus.LONG_TERM_RECOVERY
        elif self.override == "SURGEON":
            self.state = RecoveryStatus.NORMAL_OPERATION
        
        self.create_timer(0.1, self.send_current_state)

    def init_parameters(self):
        state_override_descriptor = ParameterDescriptor(
            type=rclpy.Parameter.Type.STRING,
            description='Overrides state machine to only one state. '
                        'SURGEON to only allow surgeon input, '
                        'AGENT to only allow agent input.'
        )
        self.declare_parameter('state_machine.state_override', 'NONE', descriptor=state_override_descriptor)

    def dummy_timer_callback(self):
        future = self.fetch_network_statistics()
        future.add_done_callback(self.service_callback)

    def fetch_network_statistics(self) -> Future:
        return self.client.call_async(NetworkStatistics.Request())

    def service_callback(self, future):
        # Do not update state if override is set
        if self.override != "NONE":
            return

        response = future.result()
        self.get_logger().info(f"Random double from network monitor was {response}")
        self.send_current_state()
        if self.state == RecoveryStatus.NORMAL_OPERATION:
            self.state = RecoveryStatus.LONG_TERM_RECOVERY
        else:
            self.state = RecoveryStatus.NORMAL_OPERATION

    def send_current_state(self):
        msg = RecoveryStatus()
        msg.state = self.state
        self.publisher_.publish(msg)

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
