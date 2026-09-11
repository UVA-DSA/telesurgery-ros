import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from teleop_msgs.msg import ITP, RecoveryStatus


class DummyAgent(Node):
    def __init__(self):
        super().__init__('dummy_agent')
        self.publisher = self.create_publisher(ITP, '/agent/itp_commands', 100)
        self.state_listener = self.create_subscription(RecoveryStatus, '/recovery_type', self.recovery_callback, 10)
        self.timer = self.create_timer(0.5, self.publish_dummy_itp)
        self.grasper = True
        self.state = RecoveryStatus.NORMAL_OPERATION

    # Open and close grasper0 every half second
    def publish_dummy_itp(self):
        if self.state == RecoveryStatus.NORMAL_OPERATION: return
        msg = ITP()
        if self.grasper: msg.grasp0 = 2597
        else: msg.grasp0 = self.grasper
        self.publisher.publish(msg)
        self.grasper = not self.grasper

    def recovery_callback(self, msg: RecoveryStatus):
        self.state = msg.state

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = DummyAgent()
            node.get_logger().info("Starting dummy agent. This sends agent ITP packets to /agent/itp_commands")

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
