import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Image

from teleop_msgs.msg import ITP, ArmKinematics


class ActivityRecognition(Node):
    def __init__(self):
        super().__init__('activity_recognition')
        self.video_listener = self.create_subscription(Image, '/video', self.video_callback, 10)
        self.kinematic_listener = self.create_subscription(ArmKinematics,'/kinematics', self.kinematic_callback, 10)
        self.itp_listener = self.create_subscription(ITP, '/final/itp_commands', self.itp_commands_callback, 10)
        self.latest_video_frame = None
        self.latest_kinematics = None
        self.latest_itp_commands = None

    def video_callback(self, msg):
        self.latest_video_frame = msg

    def kinematic_callback(self, msg):
        self.latest_kinematics = msg

    def itp_commands_callback(self, msg):
        self.latest_itp_commands = msg

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = ActivityRecognition()
            node.get_logger().info("Starting dummy activity recognition. This listens for video, kinematic, and ITP data.")

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
