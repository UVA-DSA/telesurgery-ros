import struct
from collections import namedtuple
from typing import List
from teleop_msgs.msg import ITP, ITPRaw


def to_msg(d: dict) -> ITP:
    msg: ITP = ITP()
    msg.sequence = d['sequence']
    msg.pactyp = d['pactyp']
    msg.version = d['version']
    msg.delx0 = d['delx0']
    msg.delx1 = d['delx1']
    msg.dely0 = d['dely0']
    msg.dely1 = d['dely1']
    msg.delz0 = d['delz0']
    msg.delz1 = d['delz1']
    msg.qx0 = d['Qx0']
    msg.qx1 = d['Qx1']
    msg.qy0 = d['Qy0']
    msg.qy1 = d['Qy1']
    msg.qz0 = d['Qz0']
    msg.qz1 = d['Qz1']
    msg.qw0 = d['Qw0']
    msg.qw1 = d['Qw1']
    msg.buttonstate0 = d['buttonstate0']
    msg.buttonstate1 = d['buttonstate1']
    msg.grasp0 = d['grasp0']
    msg.grasp1 = d['grasp1']
    msg.surgeon_mode = d['surgeon_mode']
    msg.checksum = d['checksum']
    return msg

def to_dict(msg: ITP):
    d = dict()
    d['sequence'] = msg.sequence
    d['pactyp'] = msg.pactyp
    d['version'] = msg.version
    d['delx0'] = msg.delx0
    d['delx1'] = msg.delx1
    d['dely0'] = msg.dely0
    d['dely1'] = msg.dely1
    d['delz0'] = msg.delz0
    d['delz1'] = msg.delz1
    d['Qx0'] = msg.qx0
    d['Qx1'] = msg.qx1
    d['Qy0'] = msg.qy0
    d['Qy1'] = msg.qy1
    d['Qz0'] = msg.qz0
    d['Qz1'] = msg.qz1
    d['Qw0'] = msg.qw0
    d['Qw1'] = msg.qw1
    d['buttonstate0'] = msg.buttonstate0
    d['buttonstate1'] = msg.buttonstate1
    d['grasp0'] = msg.grasp0
    d['grasp1'] = msg.grasp1
    d['surgeon_mode'] = msg.surgeon_mode
    d['checksum'] = msg.checksum
    return d

def raw_to_dict(msg: ITPRaw):
    data: List[bytes] = msg.data
    raw_bytes = b''.join(data)
    return bytes_to_dict(raw_bytes)


format_str = '<IIIiiiiiiddddddddiiiiii'
fields = 'sequence pactyp version delx0 delx1 dely0 dely1 delz0 delz1 Qx0 Qx1 Qy0 Qy1 Qz0 Qz1 Qw0 Qw1 buttonstate0 buttonstate1 grasp0 grasp1 surgeon_mode checksum'.split()
UStruct = namedtuple('UStruct', fields)

def bytes_to_dict(data: bytes):
    unpacked_data = struct.unpack(format_str, data)
    u_struct = UStruct(*unpacked_data)
    return u_struct._asdict()