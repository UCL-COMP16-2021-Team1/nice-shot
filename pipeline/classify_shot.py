import numpy as np
import cv2
import tensorflow as tf

model = tf.keras.models.load_model("../experiments/shot-recognition/cnn_recognition_model.h5")
class_names = ['amateur_backhand', 'amateur_backhand2hands', 'amateur_backhandslice', 'amateur_forehandflat', 'amateur_forehandopen', 'amateur_forslice', 'amateur_serviceflat', 'amateur_servicekick', 'amateur_serviceslice', 'amateur_smash', 'amateur_volley', 'amateur_volleybackhand', 'expert_backhand', 'expert_backhand2hands', 'expert_backhandslice', 'expert_forehandflat', 'expert_forehandopen', 'expert_forslice', 'expert_serviceflat', 'expert_servicekick', 'expert_serviceslice', 'expert_smash', 'expert_volley', 'expert_volleybackhand']

def classify_shot(skeleton_img):
    skeleton_img = cv2.resize(skeleton_img, dsize=(15, 250))
    predictions = model.predict(skeleton_img[None,...])
    return class_names[np.argmax(predictions[0])]