import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

def detect_shot_times(left_wrist_frames, right_wrist_frames):
    lw_speed_x = np.gradient(left_wrist_frames[..., 0])
    lw_speed_y = np.gradient(left_wrist_frames[..., 1])
    lw_speed_z = np.gradient(left_wrist_frames[..., 2])

    rw_speed_x = np.gradient(right_wrist_frames[..., 0])
    rw_speed_y = np.gradient(right_wrist_frames[..., 1])
    rw_speed_z = np.gradient(right_wrist_frames[..., 2])

    lw_speed = np.sqrt(lw_speed_x**2 + lw_speed_y**2 + lw_speed_z**2)
    rw_speed = np.sqrt(rw_speed_x**2 + rw_speed_y**2 + rw_speed_z**2)

    # assume swing speed at any time is maximum speed between left wrist and right wrist
    swing_speed = np.amax(np.stack([lw_speed, rw_speed]), axis=0)
    # downsample for coarser reperesentation of swing speed
    downsample_factor = 4
    swing_speed = ndimage.zoom(swing_speed, 1/downsample_factor)
    # smooth and normalise swing speed
    swing_speed = ndimage.gaussian_filter(swing_speed, sigma=2)
    swing_speed /= swing_speed.max()

    shot_threshold = 0.5
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
