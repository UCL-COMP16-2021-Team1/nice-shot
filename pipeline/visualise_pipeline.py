import cv2
import numpy as np
import mediapipe as mp
from extract_pose import extract_pose_frames
from detect_shot_times import detect_shot_times
from classify_shot import classify_shot

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

pose_frames, landmarks = extract_pose_frames(frames)
shot_times = detect_shot_times(pose_frames[:,3,0], pose_frames[:,3,0])

shot_classifications = []
for t in shot_times:
    shot_frames = pose_frames[max(0,t-20):min(len(pose_frames)-1,t+11),...]
    classification = classify_shot(shot_frames)
    shot_classifications.append(classification)

shot_counter = 0
current_shot = ""
for i in range(len(frames)):
    if shot_counter < len(shot_times) and i == shot_times[shot_counter]:
        shot_counter += 1
        current_shot = shot_classifications[shot_counter-1]

    mp_drawing.draw_landmarks(frames[i], landmarks[i], mp_pose.POSE_CONNECTIONS)
    if shot_counter > 0:
        cv2.putText(frames[i], "Player 1 shot: "+str(current_shot), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imwrite("test/"+str(i)+".png", frames[i])

"""
_, height, width, _ = frames.shape
player1_frames = frames[:, height//2:height, ...]
player2_frames = frames[:, :height//2, width//4:3*width//4, ...]

player1_pose_frames, player1_landmarks = extract_pose_frames(player1_frames)
player2_pose_frames, player2_landmarks = extract_pose_frames(player2_frames)

player1_shot_times = detect_shot_times(player1_pose_frames[:,3,0], player1_pose_frames[:,10,0])
player2_shot_times = detect_shot_times(player2_pose_frames[:,3,0], player2_pose_frames[:,10,0])

player1_shot_classifications = []

for t in player1_shot_times:
    for s in range(t-20,t+11):
        cv2.imshow("shot frame", player1_frames[s])
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    shot_frames = player1_pose_frames[t-20:t+11,...]
    classification = classify_shot(shot_frames)
    player1_shot_classifications.append(classification)

player1_shot_counter = 0
player1_current_shot = ""
for i in range(len(frames)):
    player1_frame = player1_frames[i]
    player2_frame = player2_frames[i]

    if player1_shot_counter < len(player1_shot_times) and i == player1_shot_times[player1_shot_counter]:
        player1_shot_counter += 1
        player1_current_shot = player1_shot_classifications[player1_shot_counter-1]

    mp_drawing.draw_landmarks(player1_frame, player1_landmarks[i], mp_pose.POSE_CONNECTIONS)
    mp_drawing.draw_landmarks(player2_frame, player2_landmarks[i], mp_pose.POSE_CONNECTIONS)

    frames[i, height//2:height, ...] = player1_frame
    frames[i, :height//2, width//4:3*width//4, ...] = player2_frame

    if player1_shot_counter > 0:
        cv2.putText(frames[i], "Player 1 shot: "+str(player1_current_shot), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow("annotated frame", frames[i])
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
"""
