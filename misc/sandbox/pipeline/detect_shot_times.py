import numpy as np
from scipy import signal, ndimage

def detect_shot_times(left_wrist_frames, right_wrist_frames):
    lw_speed_x = np.abs(np.gradient(left_wrist_frames[..., 0]))
    lw_speed_y = np.abs(np.gradient(left_wrist_frames[..., 1]))
    lw_speed_z = np.abs(np.gradient(left_wrist_frames[..., 2]))

    rw_speed_x = np.abs(np.gradient(right_wrist_frames[..., 0]))
    rw_speed_y = np.abs(np.gradient(right_wrist_frames[..., 1]))
    rw_speed_z = np.abs(np.gradient(right_wrist_frames[..., 2]))

    # assume swing speed at any time is maximum speed in any dimension of either wrist
    swing_speed = np.amax(np.stack(
        [lw_speed_x, lw_speed_y, lw_speed_z,
        rw_speed_x, rw_speed_y, rw_speed_z]
    ), axis=0)

    swing_speed = ndimage.gaussian_filter(swing_speed, sigma=10)
    shot_threshold = 0.1
    shot_times, _ = signal.find_peaks(swing_speed, height=shot_threshold)
    return shot_times
