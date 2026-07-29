import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from teleop_msgs.msg import RecoveryStatus


class FaultRecoveryStateMachine(Node):
    def __init__(self):
        super().__init__('fault_recovery_state_machine')
        self.publisher_ = self.create_publisher(RecoveryStatus, '/recovery_type', 10)
        self.timer = self.create_timer(10, self.dummy_timer_callback)
        self.state = RecoveryStatus.NORMAL_OPERATION

    def dummy_timer_callback(self):
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
