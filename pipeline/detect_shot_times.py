import numpy as np
from scipy import signal, ndimage
import matplotlib.pyplot as plt

def detect_shot_times(left_wrist_x, right_wrist_x):
    lw_speed = np.abs(np.gradient(left_wrist_x))
    rw_speed = np.abs(np.gradient(right_wrist_x))
    if lw_speed.max() > rw_speed.max():
        swing_speed = lw_speed
    else:
        swing_speed = rw_speed
    swing_speed = ndimage.gaussian_filter(swing_speed, sigma=5)
    shot_threshold = 0.05
    shot_times, _ = signal.find_peaks(swing_speed, height=shot_threshold)
    return shot_times
