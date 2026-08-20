import socket, time, argparse
import threading
from queue import Queue

import rclpy


class VideoStreamer:
    # parser = argparse.ArgumentParser(description="stream sender script")

    # parser.add_argument("--dir", type=str, default = r"/", help="Frames Directory")
    # parser.add_argument("--port", type = int, default = 5005, help= "port")
    # parser.add_argument("--ip", type=str, default="127.0.0.1", help="ip")
    # args = parser.parse_args()

    # imgs = os.listdir(args.dir)
    # imgs.sort()

    def __init__(self, ip, port, node):
        self.ip = ip
        self.port = port
        self.node: rclpy.node.Node = node
        # self.fps = 1.0 / 30
        self.socket = socket.socket()
        self.queue = Queue()
        self.node.get_logger().info("connecting")

        self.send_thread = threading.Thread(target=self.send_loop)
        self.send_thread.start()

    def send_loop(self):
        connected = False
        while not connected:
            try:
                self.socket.connect((self.ip, self.port))
                connected = True
            except ConnectionRefusedError:
                self.node.get_logger().info("Connection refused, retrying in 3s")
                time.sleep(3)

        while rclpy.ok():
            data = self.queue.get()
            self.socket.sendall(f"{len(data):<16}".encode())
            self.socket.sendall(data)

    def add_to_queue(self, data):
        self.queue.put(data)

    def close(self):
        self.send_thread.join()
        print("done")
        self.socket.close()
