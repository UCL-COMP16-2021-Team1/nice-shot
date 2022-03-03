import cv2
import numpy as np
import mediapipe as mp
from extract_pose import extract_pose_frames
from detect_shot_times import detect_shot_times
from classify_shot import classify_shot

def analyse_video(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    timestamps = []
    frames = []
    while cap.isOpened():
        timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    frames = np.stack(frames)

    world_pose_frames, image_pose_frames = extract_pose_frames(frames)
    shot_times = detect_shot_times(world_pose_frames[:,3,...], world_pose_frames[:,10,...])

    shot_analysis = {}
    shot_analysis["intervals"] = []
    shot_analysis["timestamps"] = []
    shot_analysis["classifications"] = []
    shot_analysis["world_poses"] = []
    shot_analysis["image_poses"] = []
    for t in shot_times:
        # assume shot takes 2 seconds
        # TODO: make shot clipping more precise?
        interval = 2 * fps
        start_t = max(0,int(t-interval))
        end_t = min(int(t+interval)+1, len(world_pose_frames)-1)
        shot_analysis["intervals"].append((start_t, end_t))
        shot_timestamps = timestamps[start_t:end_t]
        shot_timestamps = [t - shot_timestamps[0] for t in shot_timestamps]
        shot_analysis["timestamps"].append(shot_timestamps)

        world_pose = world_pose_frames[start_t:end_t]
        shot_analysis["world_poses"].append(world_pose)
        image_pose = image_pose_frames[start_t:end_t]
        shot_analysis["image_poses"].append(image_pose)
        shot = classify_shot(world_pose)[0]
        shot_analysis["classifications"].append(shot)
    
    return shot_analysis
