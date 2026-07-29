import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from teleop_msgs.msg import RecoveryStatus, ITP


class CommandSwitch(Node):
    def __init__(self):
        super().__init__('command_switch')
        self.publisher_ = self.create_publisher(ITP, '/final/itp_commands', 100)
        self.agent_listener = self.create_subscription(ITP, '/agent/itp_commands', self.agent_callback, 100)
        self.surgeon_listener = self.create_subscription(ITP, '/itp_commands', self.surgeon_callback, 100)
        self.state_listener = self.create_subscription(RecoveryStatus, '/recovery_type', self.recovery_callback, 10)

        self.state = RecoveryStatus.NORMAL_OPERATION

    def recovery_callback(self, msg: RecoveryStatus):
        self.state = msg.state

    def surgeon_callback(self, msg: ITP):
        if self.state != RecoveryStatus.NORMAL_OPERATION: return
        self.publisher_.publish(msg)

    def agent_callback(self, msg: ITP):
        if self.state == RecoveryStatus.NORMAL_OPERATION: return
        self.publisher_.publish(msg)

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = CommandSwitch()

            node.get_logger().info("Starting command switch. This listens to both surgeon and agent commands."
                                   "Depending on the state of the fault recovery state machine, it will forward one of them to /final/itp_commands.")

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
