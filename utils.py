"""This class includes various useful functions"""

import cv2
import os

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
    '.tif', '.TIF', '.tiff', '.TIFF']
VIDEOS_EXTENSIONS = ['MP4']

def resize(image, *size):
    assert len(size) > 2, 'Can not resize the image: wrong size'
    size = tuple(size)
    img = cv2.resize(image, size)

    return img
def mkdirs(paths):
    if isinstance(paths, list):
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
    elif not os.path.exists(paths):
        os.makedirs(paths)

def is_img_videos(filename):
    """Checking if the file format is image format"""
    is_img = any(filename.endswith(extension) for extension in IMG_EXTENSIONS)
    is_videos = any(filename.endswith(extension) for extension in VIDEOS_EXTENSIONS)
    return is_img, is_videos

def get_datapaths(input_dir):
    """To create dataset, we need to save paths of images"""
    image_paths = []
    assert os.path.isdir(input_dir), f"{input_dir} is not existed"

    for root, _, names in os.walk(input_dir):
        for name in names:
            path = os.path.join(root, name)
            image_paths.append(path)
    return image_paths