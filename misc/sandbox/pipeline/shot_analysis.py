import mediapipe as mp
import numpy as np
from scipy import ndimage
from classify_shot import classify_shot
import copy

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def detect_shot_times(lw_speed, rw_speed):
    # assume swing speed at any time is maximum speed between left wrist and right wrist
    swing_speed = np.amax(np.stack([lw_speed, rw_speed]), axis=0)
    # downsample for coarser reperesentation of swing speed
    downsample_factor = 4
    swing_speed = ndimage.zoom(swing_speed, 1/downsample_factor)
    # smooth swing speed
    swing_speed = ndimage.gaussian_filter(swing_speed, sigma=2)

    # find shot threshold as half a standard deviation above the mean swing speed
    shot_threshold = np.median(swing_speed) + 0.5 * np.std(swing_speed)
    
    # find shot times as zero-crossings of swing speed, offset by shot threshold
    shot_times = ((np.where(np.diff(np.sign(swing_speed-shot_threshold)))[0] + 1) * downsample_factor).tolist()
    if swing_speed[0] >= shot_threshold:
        shot_times.insert(0, 0)
    if swing_speed[-1] >= shot_threshold:
        shot_times.append(len(lw_speed)-1)
    
    shot_intervals = []
    for i in range(0, len(shot_times)-1, 2):
        shot_intervals.append((shot_times[i], shot_times[i+1]))
    return shot_intervals

def calc_joint_speed(frames):
    speed_x = np.gradient(frames[..., 0])
    speed_y = np.gradient(frames[..., 1])
    speed_z = np.gradient(frames[..., 2])
    return np.sqrt(speed_x**2 + speed_y**2 + speed_z**2)

def analyse_shots(joint_frames):
    lw_speed, rw_speed = calc_joint_speed(np.array(joint_frames["left_wrist"])), calc_joint_speed(np.array(joint_frames["right_wrist"]))
    shot_intervals = detect_shot_times(lw_speed, rw_speed)

    shot_analysis = {}
    shot_analysis["intervals"] = []
    shot_analysis["classifications"] = []
    shot_analysis["joint_frames"] = []

    for start_t, end_t in shot_intervals:
        shot_analysis["intervals"].append((start_t, end_t))
        shot_joint_frames = copy.deepcopy(joint_frames)
        for joint in shot_joint_frames.keys():
            shot_joint_frames[joint] = shot_joint_frames[joint][start_t:end_t+1]
        shot_analysis["joint_frames"].append(shot_joint_frames)
        shot = classify_shot(shot_joint_frames)[0]
        shot_analysis["classifications"].append(shot)

    return shot_analysis
