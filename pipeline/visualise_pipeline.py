import cv2
import numpy as np
import mediapipe as mp
from torch import det
from extract_pose import extract_pose_frames
from detect_shot_times import detect_shot_times
from classify_shot import classify_shot
import matplotlib.pyplot as plt

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture("test_clip.mp4")
frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
cap.release()
frames = np.array(frames)
_, height, width, _ = frames.shape
player1_frames = frames[:, height//2:height, ...]
player2_frames = frames[:, :height//2, width//4:3*width//4, ...]

player1_pose_frames, player1_landmarks = extract_pose_frames(player1_frames)
player2_pose_frames, player2_landmarks = extract_pose_frames(player2_frames)

player1_shot_times = detect_shot_times(player1_pose_frames[:,3,0], player1_pose_frames[:,10,0])
player2_shot_times = detect_shot_times(player2_pose_frames[:,3,0], player2_pose_frames[:,10,0])

player1_shot_counter = 0
player2_shot_counter = 0
for i in range(len(frames)):
    player1_frame = player1_frames[i]
    player2_frame = player2_frames[i]

    if player1_shot_counter < len(player1_shot_times) and i == player1_shot_times[player1_shot_counter]:
        player1_shot_counter += 1
    if player2_shot_counter < len(player2_shot_times) and i == player2_shot_times[player2_shot_counter]:
        player2_shot_counter += 1

    mp_drawing.draw_landmarks(player1_frame, player1_landmarks[i], mp_pose.POSE_CONNECTIONS)
    mp_drawing.draw_landmarks(player2_frame, player2_landmarks[i], mp_pose.POSE_CONNECTIONS)

    frames[i, height//2:height, ...] = player1_frame
    frames[i, :height//2, width//4:3*width//4, ...] = player2_frame

    cv2.putText(frames[i], "Player 2 shot count: "+str(player2_shot_counter), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('annotated pose', frames[i])
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

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
