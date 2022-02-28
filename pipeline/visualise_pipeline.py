import cv2
import numpy as np
import mediapipe as mp
from extract_pose import extract_pose_frames
from detect_shot_times import detect_shot_times
from classify_shot import classify_shot

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture("../experiments/shot-recognition/data/VIDEO_RGB/backhand/p25_backhand_s3.avi")
frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
cap.release()
frames = np.stack(frames)

pose_frames, landmarks = extract_pose_frames(frames)
shot_times = detect_shot_times(pose_frames[:,3,...], pose_frames[:,10,...])

shot_classifications = []
for t in shot_times:
    # assume shot takes 2 seconds for a 30fps video
    start_t = max(0,t-30)
    end_t = min(t+31,len(pose_frames)-1)

    shot_frames = frames[start_t:end_t]
    shot_pose_frames = pose_frames[start_t:end_t]
    shot_landmarks = landmarks[start_t:end_t]

    shot = classify_shot(shot_pose_frames)
    for i in range(len(shot_frames)):
        frame = shot_frames[i].copy()
        mp_drawing.draw_landmarks(frame, shot_landmarks[i], mp_pose.POSE_CONNECTIONS)
        cv2.putText(frame, "Shot: "+str(shot), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("annotated shot", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    shot_classifications.append(shot)
print(shot_classifications)
