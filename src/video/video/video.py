from rclpy.node import Node


class VideoStreamer(Node):
    def __init__(self):
        super().__init__("video")



def main() -> None:
    print('Hi from video.')


if __name__ == '__main__':
    main()
