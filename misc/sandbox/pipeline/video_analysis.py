import cv2
import json
import sys
import numpy as np
from pose_extraction import extract_joint_frames

def analyse_video(video_path, out_json_path, out_annotated_vid_path=None):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    frames = np.stack(frames)

    joint_frames = extract_joint_frames(frames)
    shot_analysis = analyse_shots(frames)
    shots_json = {
        "shots": 
        [
            {
                "start_frame_idx": int(start_t),
                "end_frame_idx": int(end_t),
                "classification": classification,
                "world_keyframes": pose2keyframes(world_pose_frames),
                "image_pose_frames": image_pose_frames.tolist()
            } for ((start_t, end_t), classification, world_pose_frames, image_pose_frames) 
            in zip(
                shot_analysis["intervals"], 
                shot_analysis["classifications"], 
                shot_analysis["world_poses"], 
                shot_analysis["image_poses"]
            )
        ]
    }
    json.dump(shots_json, open(out_path, "w"), indent=2)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("incorrect number of arguments.")
    else:
        pipeline2json(args[0], args[1])