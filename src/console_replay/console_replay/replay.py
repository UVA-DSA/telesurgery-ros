import struct
import lz4.frame
import socket
import time
import threading

import rclpy.publisher
from teleop_msgs.msg import ITPRaw

# This is an altered version of replay.py from the telesurgery-qos-analysis repository
class Replay:
    def __init__(self, filepath, node):
        self.node: rclpy.node.Node = node
        self.filepath = filepath
        self._stop_event = threading.Event()

    def replay_udp(self, dest_ip, dest_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)  # ← prevents blocking forever on send
        packet_count = 0
        start_time = time.time()

        try:
            with lz4.frame.open(self.filepath, 'rb') as f:
                previous_time = 0
                system_time = time.time()
                while not self._stop_event.is_set() and rclpy.ok():  # ← check stop flag each iteration
                    header = f.read(11)
                    if not header or len(header) < 11:
                        break
                    timestamp, length, dropped = struct.unpack('!QH?', header)
                    if length == 0:
                        break
                    packed_data = f.read(struct.calcsize(f"!{length}s"))
                    if not packed_data:
                        break
                    data = struct.unpack(f"!{length}s", packed_data)[0]

                    current_packet_time = timestamp / 1e9
                    if packet_count > 0:
                        time_delta = current_packet_time - previous_time
                        sleep_time = max(0, time_delta - (time.time() - system_time))
                        if sleep_time > 0:
                            # Interruptible sleep: wake up to check stop_event
                            self._stop_event.wait(timeout=sleep_time)

                    if self._stop_event.is_set():
                        break

                    system_time = time.time()
                    sock.sendto(data, (dest_ip, dest_port))  # ← was RECEIVER_PORT
                    packet_count += 1
                    previous_time = current_packet_time
        finally:
            sock.close()
            self.node.get_logger().info(f"Replay finished. Sent {packet_count} packets.")
            total_time = time.time() - start_time
            if total_time > 0:
                self.node.get_logger().info(f"Average frequency: {packet_count / total_time:.2f} Hz")

    def replay_ros(self, publisher: rclpy.node.Publisher):
        packet_count = 0
        with lz4.frame.open(self.filepath, 'rb') as f:
            previous_time = 0
            system_time = time.time()
            while not self._stop_event.is_set() and rclpy.ok():  # ← check stop flag each iteration
                header = f.read(11)
                if not header or len(header) < 11:
                    break
                timestamp, length, dropped = struct.unpack('!QH?', header)
                if length == 0:
                    break
                packed_data = f.read(struct.calcsize(f"!{length}s"))
                if not packed_data:
                    break
                data = struct.unpack(f"!{length}s", packed_data)[0]

                current_packet_time = timestamp / 1e9
                if packet_count > 0:
                    time_delta = current_packet_time - previous_time
                    sleep_time = max(0, time_delta - (time.time() - system_time))
                    if sleep_time > 0:
                        # Interruptible sleep: wake up to check stop_event
                        self._stop_event.wait(timeout=sleep_time)

                if self._stop_event.is_set():
                    break

                system_time = time.time()
                msg = ITPRaw()
                msg.data = data
                publisher.publish(msg)
                packet_count += 1
                previous_time = current_packet_time
        self.node.get_logger().info(f"Replay finished. Sent {packet_count} packets.")