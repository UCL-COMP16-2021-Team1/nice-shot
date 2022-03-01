import cv2
import json
import sys
import numpy
from analyse_video import analyse_video

def pipeline2json(video_path, out_path):
    cap = cv2.VideoCapture(video_path)
    shot_intervals, shot_classifications, shot_world_poses, shot_image_poses  = analyse_video(cap)
    shots_json = {
        "shots": 
        [
            {
                "start_frame_idx": int(start_t),
                "end_frame_idx": int(end_t),
                "classification": classification,
                "world_pose_frames": world_pose_frames.tolist(),
                "image_pose_frames": image_pose_frames.tolist()
            } for ((start_t, end_t), classification, world_pose_frames, image_pose_frames) in zip(shot_intervals, shot_classifications, shot_world_poses, shot_image_poses)
        ]
    }
    json.dump(shots_json, open(out_path, "w"))

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("incorrect number of arguments.")
    else:
        pipeline2json(args[0], args[1])