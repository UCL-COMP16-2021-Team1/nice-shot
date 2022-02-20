import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class PoseNotFoundError(Exception):
    pass

def format_joints(landmarks):
    joints = []
    # ordered joints as landmark indices
    # additionally includes neck and torso joints
    joint_indices = [0,13,31,15,23,25,11,"neck",14,32,16,24,26,12,"torso"]

    shoulder_l = landmarks[11]
    shoulder_r = landmarks[12]
    hip_r = landmarks[24]
    for i in joint_indices:
        if i == "neck":
            neck_x = (shoulder_l.x + shoulder_r.x) / 2
            neck_y = (shoulder_l.y + shoulder_r.y) / 2
            neck_z = (shoulder_l.z + shoulder_r.z) / 2
            joints.append([neck_x, neck_y, neck_z])
        elif i == "torso":
            torso_x = (shoulder_l.x + hip_r.x) / 2
            torso_y = (shoulder_l.y + hip_r.y) / 2
            torso_z = (shoulder_l.z + hip_r.z) / 2
            joints.append([torso_x, torso_y, torso_z])
        else:
            l = landmarks[i]
            joints.append([l.x, l.y, l.z])
    return np.array(joints)

def extract_pose_frames(frames):
    pose_frames = []
    landmarks = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame in frames:
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks is None or results.pose_world_landmarks is None:
                if len(pose_frames) == 0:
                    continue
                pose_frames.append(pose_frames[-1].copy())
                landmarks.append(landmarks[-1])
                continue

            landmarks.append(results.pose_landmarks)
            world_landmarks = results.pose_world_landmarks.landmark
            pose_frames.append(format_joints(world_landmarks))

    if len(pose_frames) == 0:
        raise PoseNotFoundError("Pose could not be detected.")
    # pad pose frames to match total frames in video
    while len(pose_frames) < len(frames):
        pose_frames.insert(0, pose_frames[0])
        landmarks.insert(0, landmarks[0])
    return np.stack(pose_frames), landmarks
    