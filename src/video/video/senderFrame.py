import os, socket, time, argparse
from queue import Queue


class VideoStreamer:
    # parser = argparse.ArgumentParser(description="stream sender script")

    # parser.add_argument("--dir", type=str, default = r"/", help="Frames Directory")
    # parser.add_argument("--port", type = int, default = 5005, help= "port")
    # parser.add_argument("--ip", type=str, default="127.0.0.1", help="ip")
    # args = parser.parse_args()

    # imgs = os.listdir(args.dir)
    # imgs.sort()

    def __init__(self, ip, port):
        # self.fps = 1.0 / 30
        self.socket = socket.socket()
        self.queue = Queue()
        print("connecting")
        connected = False
        while not connected:
            try:
                self.socket.connect((ip, port))
                connected = True
            except ConnectionRefusedError:
                print("Connection refused, retrying in 3s")
                time.sleep(3)

    def send_thread(self):
        while rclpy.ok():
            t0 = time.time()
            path = os.path.join(args.dir, name)
            with open(path, "rb") as f:
                data = f.read()
            s.sendall(f"{len(data):<16}".encode())
            s.sendall(data)
            t = time.time() - t0
            if t < fps:
                time.sleep(fps - t)


    def close(self):
        print("done")
        self.socket.close()
