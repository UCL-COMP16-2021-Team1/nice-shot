import cv2
import json
import sys
import mediapipe as mp
import numpy as np
from os.path import join
from pose_extraction import extract_joint_frames, PoseNotFoundError
from shot_analysis import analyse_shots
from pose2bvh import pose2bvh

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class AnalysisFailedError(Exception):
    pass

def analyse_video(video_path, out_dir):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    if len(frames) == 0:
        raise AnalysisFailedError("Video analysis failed because no frames could be read from the video.")

    try:
        joint_frames, mp_landmarks = extract_joint_frames(frames)
    except PoseNotFoundError:
        raise AnalysisFailedError("Video analysis failed because no pose could be detected.")

    shot_analysis = analyse_shots(joint_frames)
    analysis_json = {
        "fps": fps,
        "shots": 
        [
            {
                "start_frame_idx": int(start_t),
                "end_frame_idx": int(end_t),
                "classification": classification,
                "confidence": float(confidence),
                "joint_frames": shot_joint_frames
            } for ((start_t, end_t), (classification, confidence), shot_joint_frames) 
            in zip(
                shot_analysis["intervals"], 
                shot_analysis["classifications"], 
                shot_analysis["joint_frames"], 
            )
        ]
    }
    json_file = open(join(out_dir, "shot_analysis.json"), "w")
    json.dump(analysis_json, json_file, indent=2)
    json_file.close()

    annotated_frames = frames.copy()
    height, width, _ = annotated_frames[0].shape
    for i in range(len(shot_analysis["intervals"])):
        start_t, end_t = shot_analysis["intervals"][i]
        for j in range(start_t, end_t+1):
            mp_drawing.draw_landmarks(annotated_frames[j], mp_landmarks[j], mp_pose.POSE_CONNECTIONS)
            classification, confidence = shot_analysis["classifications"][i]
            text = f"{classification} ({str(round(100*confidence, 2))}%)"
            text_pos = (50, 70)
            cv2.putText(annotated_frames[j], text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 8, cv2.LINE_AA)  # black outline
            cv2.putText(annotated_frames[j], text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
    video_out = cv2.VideoWriter(join(out_dir, "annotated_video.mp4"), -1, fps, (width, height))
    for f in annotated_frames:
        video_out.write(f)
    video_out.release()

    pose2bvh(joint_frames, fps)
    

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("Incorrect number of arguments. First argument should be a path to a video. Second argument should be a path to an output directory.")
    else:
        analyse_video(args[0], args[1])