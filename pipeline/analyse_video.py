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

    world_pose_frames, image_pose_frames = extract_pose_frames(frames)
    shot_times = detect_shot_times(world_pose_frames[:,3,...], world_pose_frames[:,10,...])

    shot_intervals = []
    shot_classifications = []
    shot_world_poses = []
    shot_image_poses = []
    for t in shot_times:
        # assume shot takes 2 seconds for a 30fps video
        start_t = max(0,t-30)
        end_t = min(t+31,len(world_pose_frames)-1)
        shot_intervals.append((start_t, end_t))

        world_pose = world_pose_frames[start_t:end_t]
        shot_world_poses.append(world_pose)
        image_pose = image_pose_frames[start_t:end_t]
        shot_image_poses.append(image_pose)
        shot = classify_shot(world_pose)[0]
        shot_classifications.append(shot)
    
    return shot_intervals, shot_classifications, shot_world_poses, shot_image_poses
