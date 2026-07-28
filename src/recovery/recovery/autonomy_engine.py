import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from teleop_msgs.msg import ITP


class AutonomyEngine(Node):
    def __init__(self):
        super().__init__('autonomy_engine')
        self.publisher = self.create_publisher(ITP, '/agent/itp_commands', 100)
        self.timer = self.create_timer(0.5, self.publish_dummy_itp)
        self.grasper = True

    # Open and close grasper0 every half second
    def publish_dummy_itp(self):
        msg = ITP()
        msg.grasp0 = self.grasper
        self.publisher.publish(msg)
        self.grasper = not self.grasper

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = AutonomyEngine()
            node.get_logger().info("Starting dummy autonomy engine. This sends agent ITP packets to /agent/itp_commands")

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
