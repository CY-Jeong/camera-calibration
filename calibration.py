
"""This calibration package is for checking multi view chessboard and do in both
videos and pictures only chessboards"""

from config import cfg
import json
from utils import *
import cv2

if __name__ == "__main__":
    pair_2d_3d = {}
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

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
        for i in range(cfg.NUM):
            capture = cv2.VideoCapture(datapaths[i])
            ret, frame = capture.read()
            if ret == True:
                cam_num = datapaths[i].split("/")[-1].split(".")[0]
                img = cv2.resize(frame, tuple(cfg.FILE_SIZE))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                data[cam_num] = gray
                orig[cam_num] = img
    else: raise ValueError(f"The mode {cfg.MODE} is not existed ")

    data_num = len(data)
    assert data_num == cfg.VIEW1+cfg.VIEW2+cfg.VIEW3, f'the number of file is more than view number'

    for i, img in data.items():
        # Find the chess board corners
        if cfg.PATTERN == 'chessboard':
            ret, interest_points = cv2.findChessboardCorners(data[i], (cfg.WIDTH, cfg.HEIGHT), None)
            if ret == True:
                print(f"{i} view true")
                corners = cv2.cornerSubPix(gray, interest_points, (11, 11), (-1, -1), criteria)

                # If found, add object points, image points (after refining them)
                pair_2d_3d[int(i)] = []
                """ The reason why I seperate points is that image points are same coordinate any direction, but
                it is not for real object coordinate that has some directions like flat, vertical. 
                """
                if int(i) < cfg.VIEW1:
                    pair_2d_3d[int(i)].append({ '2d_points':interest_points, '3d_points':object_points_flat})

                elif cfg.VIEW1 <= int(i) < cfg.VIEW2+cfg.VIEW1:
                    pair_2d_3d[int(i)].append({ '2d_points':interest_points, '3d_points':object_points_vertical_left})
                else:
                    pair_2d_3d[int(i)].append({'2d_points': interest_points, '3d_points': object_points_vertical_right})
                img = cv2.drawChessboardCorners(orig[i], (9, 6), corners, ret)
                mkdirs(cfg.RESULT_DIR)
                cname = cfg.RESULT_DIR + f"/{i}.png"
                cv2.imwrite(cname, img)
            else:
                print(f"{i} view false")
                raise ValueError(f"{i}th is false")
        else:
            raise ValueError("Please use chessboards")

    points_3d = [pair_2d_3d[idx][0]['3d_points'] for idx in range(data_num)]
    points_2d = [pair_2d_3d[idx][0]['2d_points'] for idx in range(data_num)]

    print(f"image size : {cfg.FILE_SIZE}")
    _, cam_matrix, distortion, rot, t = \
        cv2.calibrateCamera(points_3d[:8], points_2d[:8], tuple(cfg.FILE_SIZE), None, None)
    flag = cv2.CALIB_USE_INTRINSIC_GUESS

    _, cam_matrix, distortion, rot, t = \
            cv2.calibrateCamera(points_3d, points_2d, tuple(cfg.FILE_SIZE), cam_matrix, distortion, None, None, flag)

    # save calibration
    with open(os.path.join(cfg.RESULT_DIR, cfg.FILE_NAME_INTRINSIC), 'w') as out_file:
        json.dump({'intrinsic':cam_matrix.tolist(),
                   'distortion_coefficients':distortion.squeeze().tolist()},
                  out_file)
    data = {}
    for idx in range(data_num):
        data['extrinsic'+str(idx)] = []
        data['extrinsic'+str(idx)].append({
            'rvec':rot[idx].tolist(),
            'tvec':t[idx].tolist()
        })
    with open(os.path.join(cfg.RESULT_DIR, cfg.FILE_NAME_EXTRINSIC),'w') as out_file:
            json.dump(data, out_file)

    # compute retroprojection error
    total_error = 0
    for i in range(data_num):
        impoints, _ = cv2.projectPoints(points_3d[i], rot[i], t[i],
                                          cam_matrix, distortion)
        error = cv2.norm(points_2d[i], impoints, cv2.NORM_L2)/len(impoints)
        total_error += error
    print("total error :", total_error, "mean error :", total_error/len(points_3d))


