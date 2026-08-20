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
        self.streamer = VideoStreamer('127.0.0.1', 5005, self)


    def video_cb(self, msg: Image):
        bridge = CvBridge()
        cv_frame = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        # cv2.imshow('Video', cv_frame)
        # cv2.waitKey(1)
        # convert to jpg
        _, encoded = cv2.imencode('.jpg', cv_frame)
        self.streamer.add_to_queue(encoded.tobytes())


def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = Video()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
