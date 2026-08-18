from rclpy.node import Node


class Video(Node):
    def __init__(self):
        super().__init__("video")



def main() -> None:
    print('Hi from video.')


if __name__ == '__main__':
    main()
