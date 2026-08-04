import numpy as np
from scipy.spatial.transform import Rotation

from teleop_msgs.msg import ArmKinematics


# Must be a 4x4 matrix
def to_msg(pose_matrix0: np.ndarray, pose_matrix1: np.ndarray) -> ArmKinematics:
    pos0 = pose_matrix0[:3, 3]
    rot0 = Rotation.from_matrix(pose_matrix0[:3, :3]).as_euler('xyz')
    pos1 = pose_matrix1[:3, 3]
    rot1 = Rotation.from_matrix(pose_matrix1[:3, :3]).as_euler('xyz')

    msg = ArmKinematics()
    msg.pos0_x = pos0[0]
    msg.pos0_y = pos0[1]
    msg.pos0_z = pos0[2]
    msg.rot0_x = rot0[0]
    msg.rot0_y = rot0[1]
    msg.rot0_z = rot0[2]

    msg.pos1_x = pos1[0]
    msg.pos1_y = pos1[1]
    msg.pos1_z = pos1[2]
    msg.rot1_x = rot1[0]
    msg.rot1_y = rot1[1]
    msg.rot1_z = rot1[2]

    return msg