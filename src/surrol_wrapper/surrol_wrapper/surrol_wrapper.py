import os
import importlib.util
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

########################
# Unused at the moment #
########################

class Surrol(Node):
    def __init__(self):
        super().__init__('surrol_node')

        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, 'telesurgery-qos-analysis', 'SurRol_dVTrainer', 'tests', 'multiple_scenes_console_replay.py')

        # open this file and run it here
        # todo does not work
        spec = importlib.util.spec_from_file_location("multiple_scenes_console_replay", script_path)
        qos_analysis_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(qos_analysis_mod)

def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = Surrol()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()