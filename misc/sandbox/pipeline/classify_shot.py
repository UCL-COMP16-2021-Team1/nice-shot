import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model("cnn_recognition_model.h5")
class_names = ['backhand', 'forehand', 'service', 'smash']

def classify_shot(pose_frames):
    skeleton_img = pose_frames / np.abs(pose_frames).max()
    skeleton_img = (skeleton_img+1)*127.5
    skeleton_img = tf.image.resize(skeleton_img[None, ...], [100, 15])[0, ...].numpy()

    predictions = model.predict(skeleton_img[None, ...])
    score = tf.nn.softmax(predictions[0])

    return class_names[np.argmax(score)], np.max(score)