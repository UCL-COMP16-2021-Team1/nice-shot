import cv2
import numpy as np
import mediapipe as mp
from pose_extraction import extract_pose_frames
from shots import detect_shot_times, classify_shot

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class Video:
    
    def __init__(self, cap):
        self.cap = cap
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frames = []
        self.timestamps = []
        self.world_pose_frames = []
        self.image_pose_frames = []
        self.landmarks = [] # what are landmarks?
        self.shot_times = []

    def set_frames(self):
        while self.cap.isOpened():
            self.timestamps.append(self.cap.get(cv2.CAP_PROP_POS_MSEC))
            ret, frame = self.cap.read()
            if not ret:
                break
            self.frames.append(frame)
        self.frames = np.stack(frame)

    def analyse_frames(self):
        self.world_pose_frames, self.image_pose_frames, self.landmarks = extract_pose_frames(self.frames)
        self.shot_times = detect_shot_times(self.world_pose_frames[:,3,...], self.world_pose_frames[:,10,...])

    def analyse(self):
        self.set_frames()
        self.analyse_frames()


def get_frames_timestamps(cap):
    timestamps = []
    frames = []
    while cap.isOpened():
        timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return np.stack(frames), timestamps

def get_frame_data(frames):
    world_pose_frames, image_pose_frames, landmarks = extract_pose_frames(frames)
    shot_times = detect_shot_times(world_pose_frames[:,3,...], world_pose_frames[:,10,...])
    return world_pose_frames, image_pose_frames, landmarks, shot_times

def set_shot_timestamps(start_t, end_t, video: Video):
    shot_timestamps = video.timestamps[start_t:end_t]
    return [t - shot_timestamps[0] for t in shot_timestamps]

def set_world_pose(start_t, end_t, video: Video):
    return video.world_pose_frames[start_t:end_t]

def set_image_pose(start_t, end_t, video: Video):
    return video.image_pose_frames[start_t:end_t]


def update_shot_analysis(start_t, end_t, video: Video, shot_analysis): # What is t?
    # assume shot takes 2 seconds
    # TODO: make shot clipping more precise?

    world_pose = set_world_pose(start_t, end_t, video)
    shot_analysis["world_poses"].append(world_pose)
    shot_analysis["intervals"].append((start_t, end_t))
    shot_analysis["timestamps"].append(set_shot_timestamps(start_t, end_t, video))
    shot_analysis["image_poses"].append(set_image_pose(start_t, end_t, video))
    shot = classify_shot(world_pose)[0]
    shot_analysis["classifications"].append(shot)

    shot_frames = video.frames[start_t:end_t]
    shot_landmarks = video.landmarks[start_t:end_t]
    height, width, _ = shot_frames[0].shape 
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter(str(t)+"_"+shot+".avi", fourcc, 20.0, (height, width))
    return shot, shot_analysis, shot_frames, shot_landmarks


def visualise_results(shot, shot_frames, shot_landmarks):
    for i in range(len(shot_frames)): # idk what this is so idk what to name it as a function
        frame = shot_frames[i].copy()
        mp_drawing.draw_landmarks(frame, shot_landmarks[i], mp_pose.POSE_CONNECTIONS)
        cv2.putText(frame, "Shot: "+shot, (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("annotated video", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        #out.write(frame)
    #out.release()


def analyse_shots(fps, video: Video):

    shot_analysis = {}
    shot_analysis["intervals"] = []
    shot_analysis["timestamps"] = []
    shot_analysis["classifications"] = []
    shot_analysis["world_poses"] = []
    shot_analysis["image_poses"] = []

    interval = 2 * fps

    for t in video.shot_times:
        shot, shot_analysis, shot_frames, shot_landmarks = update_shot_analysis( 
            max(0,int(t-interval)), 
            min(int(t+interval)+1, len(video.world_pose_frames)-1), 
            video, 
            shot_analysis
            ) # I don't think I'm allowed to update dictionaries like this. Would like to update the dictionary without having to return it

        visualise_results(shot, shot_frames, shot_landmarks)
    
    return shot_analysis # maybe make shot_analysis, the dictionary, a bigger object with functions? would be easier to query


def analyse_video(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    video = Video(cap)
    video.analyse()
    return analyse_shots(fps, video)
