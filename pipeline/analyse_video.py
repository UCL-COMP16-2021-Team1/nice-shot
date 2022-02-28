import cv2
import numpy as np
import mediapipe as mp
from extract_pose import extract_pose_frames
from detect_shot_times import detect_shot_times
from classify_shot import classify_shot

# pipeline entry point
def analyse_video(cap):
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    frames = np.stack(frames)

    pose_frames, _ = extract_pose_frames(frames)
    shot_times = detect_shot_times(pose_frames[:,3,...], pose_frames[:,10,...])

    shot_classifications = []
    shot_poses = []
    for t in shot_times:
        # assume shot takes 2 seconds for a 30fps video
        start_t = max(0,t-30)
        end_t = min(t+31,len(pose_frames)-1)

        pose = pose_frames[start_t:end_t]
        shot = classify_shot(pose)
        shot_poses.append(pose)
        shot_classifications.append(shot)
    
    return shot_poses, shot_classifications