# take a path to a binary file, reads packets, sends to 5001 port

import os
import struct
import lz4.frame
import socket
import time
import threading
from collections import namedtuple

class replayoverport:
    def __init__(self, filepath):
        self.EMULATOR_PORT = 36000   # ← send HERE, not to 5001
        self.RECEIVER_PORT = 5001
        self.filepath = filepath
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def replay_log(self, dest_ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)  # ← prevents blocking forever on send
        packet_count = 0
        start_time = time.time()

        with lz4.frame.open(self.filepath, 'rb') as f:
            previous_time = 0
            system_time = time.time()
            while not self._stop_event.is_set():  # ← check stop flag each iteration
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
                sock.sendto(data, (dest_ip, self.EMULATOR_PORT))  # ← was RECEIVER_PORT
                packet_count += 1
                previous_time = current_packet_time

        sock.close()
        print(f"Replay finished. Sent {packet_count} packets.")
        total_time = time.time() - start_time
        if total_time > 0:
            print(f"Average frequency: {packet_count / total_time:.2f} Hz")

scene = replayoverport(filepath=f"dVTrainer/Data/replay_data/console_data_complete_7.bin")
#scene.start()
scene.replay_log(dest_ip='127.0.0.1')
#scene.stop()