from extract_pose import extract_pose_frames, PoseNotFoundError
from os import listdir, mkdir
from os.path import isfile, isdir, join
import cv2
import numpy as np

videos_root = "data/VIDEO_RGB/"
shots = [d for d in listdir(videos_root) if isdir(join(videos_root, d))]
for s in shots:
    src_path = videos_root+s+"/"
    out_path = "data/skeleton_images/"+s+"/"
    if not isdir(out_path):
        mkdir(out_path)
    
    videos = [f for f in listdir(src_path) if isfile(join(src_path, f))]
    for v in videos:
        cap = cv2.VideoCapture(src_path+v)
        try:
            pose_frames, landmarks = extract_pose_frames(cap)
        except PoseNotFoundError:
            continue
        cap.release()

        skeleton_img = pose_frames / np.abs(pose_frames).max()
        skeleton_img = (skeleton_img+1)*127.5
        cv2.imwrite(out_path+v[:-4]+".png", skeleton_img)

