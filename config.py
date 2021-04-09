from __future__ import division
from __future__ import print_function

from easydict import EasyDict as edict
import yaml
import numpy as np


__C = edict()
cfg = __C
__C.NUM = 15                 # view number
__C.WIDTH = 9
__C.HEIGHT = 6
__C.FILE_SIZE = (1200, 900)
__C.PATTERN = 'chessboard'  # chessboard
__C.INPUT_DIR = './chessboards'
__C.RESULT_DIR = './result_dir'
__C.MODE = 'images'         # images, videos
__C.VIEW1 = 8
__C.VIEW2 = 5
__C.VIEW3 = 2
__C.FILE_NAME_INTRINSIC = "intrinsic.json"
__C.FILE_NAME_EXTRINSIC = "extrinsic.json"


"""You need to measure each one block's size and relative distance in real 3d object coordinate.
    For example, if you have some points that is ranged in (0,0,0)~(8,0,0) of with and (0,0,0)~(0,8,0) of height
    on flat chessboard, you can get some location of points that is ranged in (0,0,0)~(0,0,8) and (0,0,0)~(0,8,0) in vertical chessboard.  
    """
__C.CHESS_FLAT = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 0], [5, 0, 0], [6, 0, 0], [7, 0, 0], [8, 0, 0],
                           [0, -1, 0], [1, -1, 0], [2, -1, 0], [3, -1, 0], [4, -1, 0], [5, -1, 0], [6, -1, 0], [7, -1, 0], [8, -1, 0],
                           [0, -2, 0], [1, -2, 0], [2, -2, 0], [3, -2, 0], [4, -2, 0], [5, -2, 0], [6, -2, 0], [7, -2, 0], [8, -2, 0],
                           [0, -3, 0], [1, -3, 0], [2, -3, 0], [3, -3, 0], [4, -3, 0], [5, -3, 0], [6, -3, 0], [7, -3, 0], [8, -3, 0],
                           [0, -4, 0], [1, -4, 0], [2, -4, 0], [3, -4, 0], [4, -4, 0], [5, -4, 0], [6, -4, 0], [7, -4, 0], [8, -4, 0],
                           [0, -5, 0], [1, -5, 0], [2, -5, 0], [3, -5, 0], [4, -5, 0], [5, -5, 0], [6, -5, 0], [7, -5, 0], [8, -5, 0]], np.float32)
__C.CHESS_VERTICAL_LEFT = np.array([[0, 1.3, 0], [1, 1.3, 0], [2, 1.3, 0], [3, 1.3, 0], [4, 1.3, 0], [5, 1.3, 0], [6, 1.3, 0], [7, 1.3, 0], [8, 1.3, 0],
                              [0, 1.3, 1], [1, 1.3, 1], [2, 1.3, 1], [3, 1.3, 1], [4, 1.3, 1], [5, 1.3, 1], [6, 1.3, 1], [7, 1.3, 1], [8, 1.3, 1],
                              [0, 1.3, 2], [1, 1.3, 2], [2, 1.3, 2], [3, 1.3, 2], [4, 1.3, 2], [5, 1.3, 2], [6, 1.3, 2], [7, 1.3, 2], [8, 1.3, 2],
                              [0, 1.3, 3], [1, 1.3, 3], [2, 1.3, 3], [3, 1.3, 3], [4, 1.3, 3], [5, 1.3, 3], [6, 1.3, 3], [7, 1.3, 3], [8, 1.3, 3],
                              [0, 1.3, 4], [1, 1.3, 4], [2, 1.3, 4], [3, 1.3, 4], [4, 1.3, 4], [5, 1.3, 4], [6, 1.3, 4], [7, 1.3, 4], [8, 1.3, 4],
                              [0, 1.3, 5], [1, 1.3, 5], [2, 1.3, 5], [3, 1.3, 5], [4, 1.3, 5], [5, 1.3, 5], [6, 1.3, 5], [7, 1.3, 5], [8, 1.3, 5]], np.float32)
__C.CHESS_VERTICAL_RIGHT = np.array([[8, 1.1, 1.2], [7, 1.1, 1.2], [6, 1.1, 1.2], [5, 1.1, 1.2], [4, 1.1, 1.2], [3, 1.1, 1.2], [2, 1.1, 1.2], [1, 1.1, 1.2],[0, 1.1, 1.2],
                              [8, 1.1, 2.2], [7, 1.1, 2.2], [6, 1.1, 2.2], [5, 1.1, 2.2], [4, 1.1, 2.2], [3, 1.1, 2.2], [2, 1.1, 2.2], [1, 1.1, 2.2],[0, 1.1, 2.2],
                              [8, 1.1, 3.2], [7, 1.1, 3.2], [6, 1.1, 3.2], [5, 1.1, 3.2], [4, 1.1, 3.2], [3, 1.1, 3.2], [2, 1.1, 3.2], [1, 1.1, 3.2],[0, 1.1, 3.2],
                              [8, 1.1, 4.2], [7, 1.1, 4.2], [6, 1.1, 4.2], [5, 1.1, 4.2], [4, 1.1, 4.2], [3, 1.1, 4.2], [2, 1.1, 4.2], [1, 1.1, 4.2],[0, 1.1, 4.2],
                              [8, 1.1, 5.2], [7, 1.1, 5.2], [6, 1.1, 5.2], [5, 1.1, 5.2], [4, 1.1, 5.2], [3, 1.1, 5.2], [2, 1.1, 5.2], [1, 1.1, 5.2],[0, 1.1, 5.2],
                              [8, 1.1, 6.2], [7, 1.1, 6.2], [6, 1.1, 6.2], [5, 1.1, 6.2], [4, 1.1, 6.2], [3, 1.1, 6.2], [2, 1.1, 6.2], [1, 1.1, 6.2],[0, 1.1, 6.2]], np.float32)



def _merge_a_into_b(a, b):
    """Merge config dictionary 'a' into b."""
    assert type(a) is edict, "config 'a' is not dictionary"

    for k, v in a.items():
        if not k in b:
            raise KeyError(f'{k} is not a valid config option')

        b_type = type(b[k])
        if b_type is not type(v):
            if isinstance(b[k], np.ndarray):
                v = np.array(v, dtype=b[k].dtype)
            else:
                raise ValueError(f'type mismatch: expected {type(v)} but got {type(b[k])}')

        if type(v) is edict:
            try:
                _merge_a_into_b(a, b)
            except:
                raise KeyError(f"error in config key: {k}")
        else:
            b[k] = v
def cfg_from_file(filename):
    """Load a config file with yaml format and merge it into the options"""
    with open(filename, 'r') as f:
        yaml_cfg = edict(yaml.load(f))

    _merge_a_into_b(yaml_cfg, __C)