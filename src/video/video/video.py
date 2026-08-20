import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Image

from video.senderFrame import VideoStreamer


class Video(Node):
    def __init__(self):
        super().__init__("video")

        self.video_sub = self.create_subscription(Image, '/video', self.video_cb, 100)
        # self.streamer = VideoStreamer()


    def video_cb(self, msg: Image):
        bridge = CvBridge()
        cv_frame = bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
        cv2.imshow('Video', cv_frame)
        cv2.waitKey(1)
        # self.streamer.add_to_queue(data)


def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = Video()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
