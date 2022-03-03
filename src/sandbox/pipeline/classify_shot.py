import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model("cnn_recognition_model.h5")
class_names = ['backhand', 'backhand2hands', 'backhand_slice', 'backhand_volley', 'flat_service', 'forehand_flat', 'forehand_openstands', 'forehand_slice', 'forehand_volley', 'kick_service', 'slice_service', 'smash']

def classify_shot(pose_frames):
    skeleton_img = pose_frames / np.abs(pose_frames).max()
    skeleton_img = (skeleton_img+1)*127.5
    skeleton_img = tf.image.resize(skeleton_img[None, ...], [32, 32])[0, ...].numpy()

    predictions = model.predict(skeleton_img[None, ...])
    score = tf.nn.softmax(predictions[0])

    return class_names[np.argmax(score)], np.max(score)