import numpy as np
import tensorflow as tf
import os

model = tf.keras.models.load_model(os.path.join("analysis_pipeline/", "shot_recognition_cnn_model.h5"))
class_names = ['backhand', 'forehand', 'service', 'smash']

def classify_shot(joint_frames):
    ordered_joints = ["head",
        "left_elbow",
        "left_foot",
        "left_wrist",
        "left_hip",
        "left_knee",
        "left_shoulder",
        "neck",
        "right_elbow",
        "right_foot",
        "right_wrist",
        "right_hip",
        "right_knee",
        "right_shoulder",
        "torso"
    ]
    pose_frames = [np.array(joint_frames[joint]) for joint in ordered_joints]
    pose_img = np.stack(pose_frames)
    pose_img = pose_img.swapaxes(0,1)

    skeleton_img = pose_img / np.abs(pose_img).max()
    skeleton_img = (skeleton_img+1)*127.5
    skeleton_img = tf.image.resize(skeleton_img[None, ...], [100, 15])[0, ...].numpy()

    predictions = model.predict(skeleton_img[None, ...])
    score = tf.nn.softmax(predictions[0])

    return class_names[np.argmax(score)], np.max(score)
