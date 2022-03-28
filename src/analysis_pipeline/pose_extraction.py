import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

class PoseNotFoundError(Exception):
    pass

def format_landmark_joints(landmarks):
    joints = []
    # ordered joints as mp landmark indices
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
    return joints

def extract_pose_frames(frames):
    pose_frames = []
    mp_landmarks = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame in frames:
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks is None or results.pose_world_landmarks is None:
                # pad missing pose frame
                if len(pose_frames) == 0:
                    continue    # we'll pad missing pose frames at the start later
                pose_frames.append(pose_frames[-1].copy())
                mp_landmarks.append(mp_landmarks[-1])
                continue
            
            world_landmarks = results.pose_world_landmarks.landmark
            pose_frames.append(np.array(format_landmark_joints(world_landmarks)))
            mp_landmarks.append(results.pose_landmarks)

    if len(pose_frames) == 0:
        raise PoseNotFoundError("Pose could not be detected.")
    # pad pose frames at start to match total frames in video
    while len(pose_frames) < len(frames):
        pose_frames.insert(0, pose_frames[0])
        mp_landmarks.insert(0, mp_landmarks[0])
    
    pose_img = np.stack(pose_frames)
    return pose_img, mp_landmarks

def extract_joint_frames(frames):
    pose_img, mp_landmarks = extract_pose_frames(frames)
    joint_frames = {
        "head": pose_img[:,0,...].tolist(),
        "left_elbow": pose_img[:,1,...].tolist(),
        "left_foot": pose_img[:,2,...].tolist(),
        "left_wrist": pose_img[:,3,...].tolist(),
        "left_hip": pose_img[:,4,...].tolist(),
        "left_knee": pose_img[:,5,...].tolist(),
        "left_shoulder": pose_img[:,6,...].tolist(),
        "neck": pose_img[:,7,...].tolist(),
        "right_elbow": pose_img[:,8,...].tolist(),
        "right_foot": pose_img[:,9,...].tolist(),
        "right_wrist": pose_img[:,10,...].tolist(),
        "right_hip": pose_img[:,11,...].tolist(),
        "right_knee": pose_img[:,12,...].tolist(),
        "right_shoulder": pose_img[:,13,...].tolist(),
        "torso": pose_img[:,14,...].tolist()
    }
    return joint_frames, mp_landmarks
    