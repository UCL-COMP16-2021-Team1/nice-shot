import tensorflow as tf
import numpy as np
import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

img_height = 250
img_width = 15

shot = tf.keras.utils.load_img(
    "joints_img.png", target_size=(img_height, img_width)
)

shot_array = tf.keras.utils.img_to_array(shot)
shot_array = tf.expand_dims(shot_array, 0)

class_names = ['amateur_backhand', 'amateur_backhand2hands', 'amateur_backhandslice', 'amateur_forehandflat', 'amateur_forehandopen', 'amateur_forslice', 'amateur_serviceflat', 'amateur_servicekick', 'amateur_serviceslice', 'amateur_smash', 'amateur_volley', 'amateur_volleybackhand', 'expert_backhand', 'expert_backhand2hands', 'expert_backhandslice', 'expert_forehandflat', 'expert_forehandopen', 'expert_forslice', 'expert_serviceflat', 'expert_servicekick', 'expert_serviceslice', 'expert_smash', 'expert_volley', 'expert_volleybackhand']

model = tf.keras.models.load_model("shot-recognition/cnn_recognition_model.h5")
predictions = model.predict(shot_array)

pred = class_names[np.argmax(predictions[0])]
print(pred, np.max(predictions[0]))

cap = cv2.VideoCapture("avatar-extraction/p1_backhand_s2.mp4")
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    frameCounter = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)               

            cv2.putText(image, "Shot: "+pred, (10,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow("shot", image)
            
            frameCounter += 1

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break