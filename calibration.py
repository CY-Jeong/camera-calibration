
__author__ = "Salim Kayal"
__copyright__ = "Copyright 2016, Idiap Research Institute"
__version__ = "1.0"
__maintainer__ = "Salim Kayal"
__email__ = "salim.kayal@idiap.ch"
__status__ = "Production"
__license__ = "GPLv3"
__modifier__ = 'ChanYang Jeong'

"""This calibration package is modified from me to check multi view chessboard and do in both
videos and pictures only chessboards"""

from config import cfg
import json
from utils import *
import cv2

if __name__ == "__main__":
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    points_pair = {}  # 2d points in image plane.
    to_del = []
    flag = 0

    object_points_flat = cfg.CHESS_FLAT
    object_points_vertical_left = cfg.CHESS_VERTICAL_LEFT
    object_points_vertical_right = cfg.CHESS_VERTICAL_RIGHT

    datapaths = get_datapaths(cfg.INPUT_DIR)

    is_img = []
    is_video = []
    for v in datapaths:
        a, b = is_img_videos(v)
        is_img.append(a)
        is_video.append(b)

    data = {}
    orig = {}
    if cfg.MODE == 'images':
        assert any(is_img), 'there is any other image format'
        for i in range(cfg.NUM):
            cam_num = datapaths[i].split("/")[-1].split(".")[0]
            img = cv2.imread(datapaths[i])
            img = cv2.resize(img, tuple(cfg.FILE_SIZE))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            data[cam_num] = gray
            orig[cam_num] = img
    elif cfg.MODE == 'videos':
        data = []
        for i in range(cfg.NUM):
            capture = cv2.VideoCapture(datapaths[i])
            ret, frame = capture.read()
            if ret == True:
                cam_num = datapaths[i].split("/")[-1].split(".")[0]
                frame = cv2.resize(frame, cfg.FILE_SIZE)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                data[cam_num] = gray
    else: raise ValueError(f"The mode {cfg.MODE} is not existed ")

    data_num = len(data)
    assert data_num == cfg.VIEW1+cfg.VIEW2+cfg.VIEW3, f'the number of file is more than view number'

    for i, img in data.items():
        # Find the chess board corners
        if cfg.PATTERN == 'chessboard':
            ret, interest_points = cv2.findChessboardCorners(data[i], (cfg.WIDTH, cfg.HEIGHT), None)
            if ret == True:
                print(f"{i} view true")
                cv2.cornerSubPix(gray, interest_points, (11, 11), (-1, -1), criteria)
            else:
                print(f"{i} view false")

        # If found, add object points, image points (after refining them)
        if ret == True:
            corners2 = cv2.cornerSubPix(gray, interest_points, (11, 11), (-1, -1), criteria)
            points_pair[int(i)] = []
            """ The reason why I seperate points is that image points are same coordinate any direction, but
            it is not for real object coordinate that has some directions like flat, vertical. 
            """
            if int(i) < cfg.VIEW1:
                points_pair[int(i)].append({
                'image_points':interest_points,
                'object_points':object_points_flat
                })

            elif cfg.VIEW1 <= int(i) < cfg.VIEW2+cfg.VIEW1:
                points_pair[int(i)].append({
                'image_points':interest_points,
                'object_points':object_points_vertical_left
                })
            else:
                points_pair[int(i)].append({
                'image_points': interest_points,
                'object_points': object_points_vertical_right
                })
            img = cv2.drawChessboardCorners(orig[i], (9, 6), corners2, ret)
            mkdirs(cfg.RESULT_DIR)
            cname = cfg.RESULT_DIR + f"/{i}.png"
            cv2.imwrite(cname, img)
        else:
            to_del.append(i)
    while len(to_del) > 0:
        last_item = to_del[-1]
        del data[last_item]
        del to_del[-1]

    opoints = [points_pair[idx][0]['object_points'] for idx in range(data_num)]
    ipoints = [points_pair[idx][0]['image_points'] for idx in range(data_num)]

    print(f"image size : {cfg.FILE_SIZE}")
    _, cam_matrix, distortion, rotation_vectors, translation_vectors = \
        cv2.calibrateCamera(opoints[:8], ipoints[:8], tuple(cfg.FILE_SIZE), None, None)
    flag = flag+cv2.CALIB_USE_INTRINSIC_GUESS

    _, cam_matrix, distortion, rotation_vectors, translation_vectors = \
            cv2.calibrateCamera(opoints, ipoints, tuple(cfg.FILE_SIZE), cam_matrix, distortion, None, None, flag)

    # save calibration
    with open(os.path.join(cfg.RESULT_DIR, cfg.FILE_NAME_INTRINSIC), 'w') as out_file:
        json.dump({'intrinsic':cam_matrix.tolist(),
                   'distortion_coefficients':distortion.squeeze().tolist()},
                  out_file)
    data = {}
    for idx in range(data_num):
        data['extrinsic'+str(idx)] = []
        data['extrinsic'+str(idx)].append({
            'rvec':rotation_vectors[idx].tolist(),
            'tvec':translation_vectors[idx].tolist()
        })
    with open(os.path.join(cfg.RESULT_DIR, cfg.FILE_NAME_EXTRINSIC),'w') as out_file:
            json.dump(data, out_file)

    # compute retroprojection error
    tot_error = 0
    for i in range(12):
        ipoints2, _ = cv2.projectPoints(opoints[i], rotation_vectors[i], translation_vectors[i],
                                          cam_matrix, distortion)
        error = cv2.norm(ipoints[i],ipoints2, cv2.NORM_L2)/len(ipoints2)
        tot_error += error
    print("total error :", tot_error, "mean error :", tot_error/len(opoints))


