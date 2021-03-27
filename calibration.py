
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
import cv2
import json
from utils import *

if __name__ == "__main__":
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    points_pair = {}  # 2d points in image plane.
    to_del = []
    output_images = []
    flag = 0

    object_points_flat = cfg.CHESS_FLAT
    object_points_vertical_left = cfg.CHESS_VERTICAL_LEFT
    object_points_vertical_right = cfg.CHESS_VERTICAL_RIGHT

    datapaths = get_datapaths(cfg.INPUT_DIR)

    is_img = []
    is_video = []
    for v in range(len(datapaths)):
        a, b = is_img_videos(v)
        is_img.append(a)
        is_video.append(b)

    if cfg.MODE == 'images':
        assert any(is_img), 'there is any other image format'
        data = datapaths
    elif cfg.MODE == 'videos':
        data = []
        for i in range(cfg.NUM):
            data.append(cv2.VideoCapture(datapaths[i]))
    else: raise ValueError(f"The mode {cfg.MODE} is not existed ")

    data_num = len(data)
    assert data_num > cfg.VIEW1+cfg.VIEW2+cfg.VIEW3, f'the number of file is more than view number'

    for i, fname in enumerate(data_num):
        # print fname
        cam_num = fname.split("/")[-1].split(".")[0]
        img = cv2.imread(fname)
        img = cv2.resize(img, (1200,900))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        if cfg.PATTERN == 'chessboard':
            ret, interest_points = cv2.findChessboardCorners(gray, (cfg.WIDTH, cfg.HEIGHT), None)
            if ret == True:
                print(f"{fname} true")
                cv2.cornerSubPix(gray, interest_points, (11, 11), (-1, -1), criteria)
            else:
                print(f"{fname} false")

        # If found, add object points, image points (after refining them)
        if ret == True:
            corners2 = cv2.cornerSubPix(gray, interest_points, (11, 11), (-1, -1), criteria)
            points_pair[cam_num] = []
            """ The reason why I seperate points is that image points are same coordinate any direction, but
            it is not for real object coordinate that has some directions like flat, vertical. 
            """
            if int(cam_num) < cfg.VIEW1:
                points_pair[cam_num].append({
                'image_points':interest_points,
                'object_points':object_points_flat
                })

            elif cfg.VIEW1 <= int(cam_num) < cfg.VIEW2:
                points_pair[cam_num].append({
                'image_points':interest_points,
                'object_points':object_points_vertical_left
                })
            else:
                points_pair[cam_num].append({
                'image_points': interest_points,
                'object_points': object_points_vertical_right
                })
            img = cv2.drawChessboardCorners(img, (9, 6), corners2, ret)
            cname = cfg.RESULT_DIR + "/" + fname.split("/")[-1]
            output_images.append(img)
            cv2.imwrite(cname, img)
        else:
            to_del.append(i)
    while len(to_del) > 0:
        last_item = to_del[-1]
        del data[last_item]
        del to_del[-1]

    opoints = [points_pair[str(idx)][0]['object_points'] for idx in range(data_num)]
    ipoints = [points_pair[str(idx)][0]['image_points'] for idx in range(data_num)]
    wopoints = [points_pair[str(idx)][0]['object_points'].tolist() for idx in range(data_num)]
    wipoints = [points_pair[str(idx)][0]['image_points'].tolist() for idx in range(data_num)]
    image_resolution = cv2.imread(data[0]).shape[:-1][::-1]
    print(f"image size : {image_resolution}")
    _, cam_matrix, distortion, rotation_vectors, translation_vectors = \
        cv2.calibrateCamera(opoints[:8], ipoints[:8], image_resolution, None, None)
    flag = flag+cv2.CALIB_USE_INTRINSIC_GUESS

    _, cam_matrix, distortion, rotation_vectors, translation_vectors = \
            cv2.calibrateCamera(opoints, ipoints, image_resolution, cam_matrix, distortion, None, None, flag)

    # save calibration
    with open(os.join(cfg.RESULT_DIR, cfg.FILE_NAME_INTRINSIC), 'w') as out_file:
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
    with open(os.join(cfg.RESULT_DIR, cfg.FILE_NAME_EXTRINSIC),'w') as out_file:
            json.dump(data, out_file)
    # with open(cfg.RESULT_DIR+"/3dpoints.json", 'w') as out_points_file:
    #     json.dump({'object_points':wopoints,
    #                'image_points':wipoints},out_points_file)


    # compute retroprojection error
    tot_error = 0
    for i in range(12):
        ipoints2, _ = cv2.projectPoints(opoints[i], rotation_vectors[i], translation_vectors[i],
                                          cam_matrix, distortion)
        error = cv2.norm(ipoints[i],ipoints2, cv2.NORM_L2)/len(ipoints2)
        tot_error += error
    print("total error :", tot_error, "mean error :", tot_error/len(opoints))


