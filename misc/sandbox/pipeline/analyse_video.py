import cv2
import numpy as np
import mediapipe as mp
from extract_pose import extract_pose_frames
from detect_shot_times import detect_shot_times
from classify_shot import classify_shot

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def analyse_video(cap):
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    frames = np.stack(frames)

    world_pose_frames, image_pose_frames, landmarks = extract_pose_frames(frames)
    left_wrist_frames = world_pose_frames[:,3,...]
    right_wrist_frames = world_pose_frames[:,10,...]
    shot_intervals = detect_shot_times(left_wrist_frames, right_wrist_frames)

    shot_analysis = {}
    shot_analysis["intervals"] = []
    shot_analysis["classifications"] = []
    shot_analysis["world_poses"] = []
    shot_analysis["image_poses"] = []
    for start_t, end_t in shot_intervals:
        shot_analysis["intervals"].append((start_t, end_t))

        world_pose = world_pose_frames[start_t:end_t]
        shot_analysis["world_poses"].append(world_pose)

        image_pose = image_pose_frames[start_t:end_t]
        shot_analysis["image_poses"].append(image_pose)

        shot = classify_shot(world_pose)[0]
        shot_analysis["classifications"].append(shot)

        shot_frames = frames[start_t:end_t]
        shot_landmarks = landmarks[start_t:end_t]
        for i in range(len(shot_frames)):
            frame = shot_frames[i].copy()
            mp_drawing.draw_landmarks(frame, shot_landmarks[i], mp_pose.POSE_CONNECTIONS)
            cv2.putText(frame, "Shot: "+shot, (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("annotated video", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    return shot_analysis
