import numpy as np
import tensorflow as tf
from scipy import signal, ndimage

model = tf.keras.models.load_model("cnn_recognition_model.h5")
class_names = ['backhand', 'backhand2hands', 'backhand_slice', 'backhand_volley', 'flat_service', 'forehand_flat', 'forehand_openstands', 'forehand_slice', 'forehand_volley', 'kick_service', 'slice_service', 'smash']

def classify_shot(pose_frames):
    skeleton_img = pose_frames / np.abs(pose_frames).max()
    skeleton_img = (skeleton_img+1)*127.5
    skeleton_img = tf.image.resize(skeleton_img[None, ...], [32, 32])[0, ...].numpy()

    predictions = model.predict(skeleton_img[None, ...])
    score = tf.nn.softmax(predictions[0])

    return class_names[np.argmax(score)], np.max(score)

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