import os
import struct
import threading
import time
from collections import deque

import lz4.frame
import rclpy


class PacketWriter:

    def __init__(self, node: rclpy.node.Node):
        self.node: rclpy.node.Node = node
        self.log_path = os.path.join(os.getcwd(), 'bin_replay')
        self.log_queue = deque()
        self.log_event = threading.Event()
        self.log_lock = threading.Lock()
        self.packet_writer_thread = threading.Thread(target=self._packet_writer, daemon=False)

        self.started = False
        self.running = False

    def _packet_writer(self):
        """Write logged packets to compressed binary file"""
        with lz4.frame.open(self.log_path, 'wb') as f:
            while self.running:
                # Wait for new packets or check every second
                self.log_event.wait(timeout=1.0)
                self.log_event.clear()

                # Write any queued packets
                while True:
                    with self.log_lock:
                        # check if empty
                        if not self.log_queue:
                            break
                        timestamp, length, dropped, data = self.log_queue.popleft()

                    # Write packet header: timestamp (8 bytes), length (2 bytes), dropped flag (1 byte)
                    header = struct.pack("!QH?", timestamp, length, dropped)
                    f.write(header)

                    # Write packet data
                    f.write(struct.pack(f"!{length}s", data))

            # Flush remaining items in queue before closing file
            while True:
                with self.log_lock:
                    # check if empty
                    if not self.log_queue:
                        break
                    timestamp, length, dropped, data = self.log_queue.popleft()

                header = struct.pack("!QH?", timestamp, length, dropped)
                f.write(header)
                f.write(struct.pack(f"!{length}s", data))


    def process_packets(self, data: bytes):
        timestamp = time.time_ns()
        entry = (timestamp, len(data), False, data)
        with self.log_lock:
            self.log_queue.append(entry)
            self.log_event.set()

        if not self.started:
            self.node.get_logger().info("Packet Writer Logger starting!")
            self.started = True
            self.running = True
            self.packet_writer_thread.start()

    def stop(self):
        if self.started and self.running:
            self.running = False
            self.log_event.set()  # Wake thread up so it can drain queue and close file
            if self.packet_writer_thread and self.packet_writer_thread.is_alive():
                self.packet_writer_thread.join(timeout=3.0)