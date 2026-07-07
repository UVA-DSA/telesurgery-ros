import numpy as np
import rclpy
from rclpy import Node
from rclpy.executors import ExternalShutdownException

from teleop_msgs import ITP

class Transform(Node):
    def __init__(self):
        super().__init__('transform')
        self.ITP_sub = self.create_subscription(
            ITP,
            '/itp_comamnds',
            self.ITP_callback,
            10)

        # transformation-related fields
        self.mapping_ratio = 2 / 2458
        self.delta_pos_0_sum = np.zeros(3)
        self.delta_rot_0_sum = np.zeros(3)
        self.delta_pos_1_sum = np.zeros(3)
        self.delta_rot_1_sum = np.zeros(3)


    def ITP_callback(self, msg: ITP):
        pass

    def transform_console_data(self):
        delta_pos_0 = self.position_transform(self.delta_pos_0_sum)
        delta_pos_1 = self.position_transform(self.delta_pos_1_sum)

        delta_rot_0 = self.orientation_transform(self.delta_rot_0_sum)
        delta_rot_1 = self.orientation_transform(self.delta_rot_1_sum)

        gripper_0 = self.map_grasper(self._left_val)
        gripper_1 = self.map_grasper(self._right_val)

        return [delta_pos_0, delta_rot_0, delta_pos_1, delta_rot_1, gripper_0, gripper_1]

    def get_psm_vars(self, command, index):
        deltaX = command[f'delx{index}']
        deltaY = command[f'dely{index}']
        deltaZ = command[f'delz{index}']

        deltaQx = command[f'Qx{index}']
        deltaQy = command[f'Qy{index}']
        deltaQz = command[f'Qz{index}']

        delta_grasp = command[f'grasp{index}']

        return ((deltaX, deltaY, deltaZ), (deltaQx, deltaQy, deltaQz), delta_grasp)

    def get_packet_data(self, command):
        sequence = command[f'sequence']
        surgeon_mode = command[f'surgeon_mode']

        return sequence, surgeon_mode

    def update_delta_variables_dual(self, sequence, delta_position0, delta_position1, delta_orientation0,
                                    delta_orientation1, delta_grasp0, delta_grasp1, surgeon_mode):
        self._left_val = delta_grasp0
        self._right_val = delta_grasp1

        delta_pos_0 = np.array(delta_position0)
        delta_rot_0 = np.array(delta_orientation0)
        delta_pos_1 = np.array(delta_position1)
        delta_rot_1 = np.array(delta_orientation1)

        if not np.all(delta_pos_0 == np.zeros(3)):
            self.delta_pos_0_sum += delta_pos_0

        if not np.all(delta_rot_0 == np.zeros(3)):
            self.delta_rot_0_sum += delta_rot_0

        if not np.all(delta_pos_1 == np.zeros(3)):
            self.delta_pos_1_sum += delta_pos_1

        if not np.all(delta_rot_1 == np.zeros(3)):
            self.delta_rot_1_sum += delta_rot_1

    def position_transform(self, delta_pos):
        P_transform = np.array([[-1, 0, 0],
                                [0, 1, 0],
                                [0, 0, -1]])

        delta_pos = delta_pos * 0.01
        new_delta_pos = P_transform @ delta_pos

        return new_delta_pos

    def orientation_transform(self, delta_rot):
        R_transform = np.array([[0, 1, 0],
                                [1, 0, 0],
                                [0, 0, 1]])

        delta_rot = delta_rot * 0.2
        new_delta_rot = R_transform @ delta_rot

        return new_delta_rot

    def map_grasper(self, grasp_i):
        return 1 - (grasp_i * self.mapping_ratio)


def main(args=None) -> None:
    try:
        with rclpy.init(args=args):
            node = Transform()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
