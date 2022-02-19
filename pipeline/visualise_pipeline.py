import cv2
import mediapipe as mp
from extract_players import extract_players
from extract_pose import extract_pose_frames
from classify_shot import classify_shot

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

video_path = "test_clip.mp4"
cap = cv2.VideoCapture(video_path)

extract_players(cap)
"""
pose_frames, landmarks = extract_pose_frames(cap)

#shot_pred, score = classify_shot(pose_frames)
#print(shot_pred, score)

cap = cv2.VideoCapture(video_path)
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    mp_drawing.draw_landmarks(frame, landmarks[frame_count], mp_pose.POSE_CONNECTIONS)
    #cv2.putText(frame, "Shot: "+shot_pred, (10,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('annotated pose', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    frame_count += 1
cap.release()
"""
