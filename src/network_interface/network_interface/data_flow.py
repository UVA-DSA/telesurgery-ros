import queue
import socket
import threading
from queue import Queue

import rclpy
from std_msgs.msg import Int32

from teleop_msgs.msg import ITPRaw, ITP
from teleop_msgs_helpers import ITP_helpers


class DataFlow:
    def __init__(self, node: rclpy.node.Node):
        self.node: rclpy.Node = node

        self.fault_injector_enabled = self.node.get_parameter('enable_fault_injector').get_parameter_value().bool_value
        self.ip = self.node.get_parameter('data_flow.udp_ip').get_parameter_value().string_value
        self.port = self.node.get_parameter('data_flow.udp_port').get_parameter_value().integer_value
        self.listen_topic = self.node.get_parameter('data_flow.listen_topic_name').get_parameter_value().string_value
        self.publish_topic = self.node.get_parameter('data_flow.publish_topic_name').get_parameter_value().string_value
        self.fault_injector_in_topic = self.node.get_parameter('fault_injector_in_topic').get_parameter_value().string_value
        self.fault_injector_out_topic = self.node.get_parameter('fault_injector_out_topic').get_parameter_value().string_value

        self.sock = None
        self.itp_publisher = None
        self.initial_subscription = None

        self.publish_thread = threading.Thread(target=self.publish_itp, daemon=True)
        self.udp_listen_thread = threading.Thread(target=self.udp_listener_loop, daemon=True)
        self.publish_fault_injector_thread = threading.Thread(target=self.publish_to_injector_loop, daemon=True)
        self.profiler_thread = threading.Thread(target=self.profiler_loop, daemon=True)

        self.output_queue: Queue = queue.Queue()
        self.fault_injector_queue: Queue = queue.Queue()
        self.profiler_queue: Queue = queue.Queue()

        self.fault_injector_publisher = None
        self.fault_injector_subscription = None
        self.profiler_publisher = None

    # IO init methods

    def init_output(self):
        self.itp_publisher = self.node.create_publisher(
            ITP, self.publish_topic, 100)
        self.publish_thread.start()

    def init_profiler_out(self):
        self.profiler_publisher = self.node.create_publisher(Int32, '/profiler/first_received', 10)
        self.profiler_thread.start()

    def init_fault_injector_io(self):
        self.fault_injector_subscription = self.node.create_subscription(
            ITP, self.fault_injector_out_topic, self.fault_injector_itp_raw_callback, 100)
        self.fault_injector_publisher = self.node.create_publisher(
            ITP, self.fault_injector_in_topic, 100)
        self.publish_fault_injector_thread.start()

    def init_udp_io(self):
        # Create a UDP socket and the data struct ----------------------------------------------------
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)
        self.sock.bind((self.ip, self.port))
        self.node.get_logger().info(f"Initialized a UDP server on IP: {self.ip} and port: {self.port}")
        self.node.get_logger().info("Listening for incoming data:")

        self.udp_listen_thread.start()
        self.init_output()
        if self.fault_injector_enabled:
            self.init_fault_injector_io()

    def init_ros_io(self):
        self.initial_subscription = self.node.create_subscription(
            ITPRaw, self.listen_topic, self.itp_raw_callback, 100)
        self.init_output()

        if self.fault_injector_enabled:
            self.init_fault_injector_io()

    # loops
    def udp_listener_loop(self):
        # Taken from Console.py
        while rclpy.ok():
            try:
                data, addr = self.sock.recvfrom(1024)  # Buffer size of 1024 bytes
                command = ITP_helpers.bytes_to_dict(data)
                if self.fault_injector_enabled:
                    self.fault_injector_queue.put(command)
                else:
                    self.output_queue.put(command)

                if self.profiler_thread.is_alive():
                    self.profiler_queue.put(command)

            except socket.timeout:
                # Timeout reached, continue listening
                continue
            except Exception as e:
                self.node.get_logger().error(f"Error receiving packet: {e}")
                # self.get_logger().error(traceback.format_exc())

    def publish_to_injector_loop(self):
        while rclpy.ok():
            command = self.fault_injector_queue.get()
            msg = ITP_helpers.to_msg(command)
            self.fault_injector_publisher.publish(msg)

    def profiler_loop(self):
        while rclpy.ok():
            command = self.profiler_queue.get()
            msg = Int32()
            msg.data = command['sequence']
            self.profiler_publisher.publish(msg)

    # Receive from replay node via ROS
    def itp_raw_callback(self, msg: ITPRaw):
        command = ITP_helpers.raw_to_dict(msg)
        if self.fault_injector_enabled:
            self.fault_injector_queue.put(command)
        else:
            self.output_queue.put(command)

        if self.profiler_thread.is_alive():
            self.profiler_queue.put(command)

    # Receive from fault injector
    def fault_injector_itp_raw_callback(self, msg: ITP):
        self.output_queue.put(msg)

    # Output
    def publish_itp(self):
        while rclpy.ok():
            command = self.output_queue.get()
            if isinstance(command, ITP):
                self.itp_publisher.publish(command)
            elif isinstance(command, dict):
                msg = ITP_helpers.to_msg(command)
                self.itp_publisher.publish(msg)
            else:
                self.node.get_logger().warning("Received unknown command type when publishing ITP commands")

    def stop(self):
        if self.publish_thread.is_alive(): self.publish_thread.join(timeout=1.0)
        if self.udp_listen_thread.is_alive(): self.udp_listen_thread.join(timeout=1.0)
        if self.publish_fault_injector_thread.is_alive(): self.publish_fault_injector_thread.join(timeout=1.0)
        if self.sock:
            self.sock.close()