from extract_pose_from_video import extract_pose_frames, PoseNotFoundError
from os import listdir, mkdir
from os.path import isfile, isdir, join
import cv2
import numpy as np

def process_shot_dirs(shot_dirs, out_dir):
    root_dir = "data/VIDEO_RGB/"
    if not isdir(out_dir):
        mkdir(out_dir)
    for s in shot_dirs:
        src_path = root_dir+s+"/"
        videos = [f for f in listdir(src_path) if isfile(join(src_path, f))]
        for v in videos:
            cap = cv2.VideoCapture(src_path+v)
            try:
                pose_frames = extract_pose_frames(cap)
                cap.release()
            except PoseNotFoundError:
                cap.release()
                continue

            skeleton_img = pose_frames / np.abs(pose_frames).max()
            skeleton_img = (skeleton_img+1)*127.5
            skeleton_img = cv2.cvtColor(np.float32(skeleton_img), cv2.COLOR_RGB2BGR)
            
            cv2.imwrite(out_dir+v[:-4]+".png", skeleton_img)
            print(v)

backhand_dirs = ["backhand", "backhand_slice", "backhand_volley", "backhand2hands"]
forehand_dirs = ["forehand_flat", "forehand_openstands", "forehand_slice", "forehand_volley"]
service_dirs = ["flat_service", "kick_service", "slice_service"]
smash_dirs = ["smash"]

process_shot_dirs(backhand_dirs, "data/skeleton_images/backhand/")
process_shot_dirs(forehand_dirs, "data/skeleton_images/forehand/")
process_shot_dirs(service_dirs, "data/skeleton_images/service/")
process_shot_dirs(smash_dirs, "data/skeleton_images/smash/")