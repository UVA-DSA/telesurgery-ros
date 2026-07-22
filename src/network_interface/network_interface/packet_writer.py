import os
import struct
import threading
import time
from collections import deque

import lz4.frame


class PacketWriter:

    def __init__(self):
        self.log_path = os.path.join(os.getcwd(), 'bin_replay')
        self.log_queue = deque()
        self.log_event = threading.Event()
        self.log_lock = threading.Lock()
        self.packet_writer_thread = threading.Thread(target=self._packet_writer, daemon=True)

    def _packet_writer(self):
        """Write logged packets to compressed binary file"""
        with lz4.frame.open(self.log_path, 'wb') as f:
            while len(self.log_queue) > 0:
                # Wait for new packets or check every second
                self.log_event.wait(timeout=1.0)
                self.log_event.clear()

                # Write any queued packets
                while len(self.log_queue) > 0:
                    with self.log_lock:
                        timestamp, length, dropped, data = self.log_queue.popleft()

                    # Write packet header: timestamp (8 bytes), length (2 bytes), dropped flag (1 byte)
                    header = struct.pack("!QH?", timestamp, length, dropped)
                    f.write(header)

                    # Write packet data
                    f.write(struct.pack(f"!{length}s", data))


    def process_packets(self, data: bytes):
        timestamp = time.time_ns()
        entry = (timestamp, len(data), False, data)

        with self.log_lock:
            self.log_queue.append(entry)
            self.log_event.set()