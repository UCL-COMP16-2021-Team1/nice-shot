import cv2
import json
import sys
from analyse_video import analyse_video

def pose2keyframes(pose):
    keyframes = {
        "head": pose[:,0,...].tolist(),
        "left_elbow": pose[:,1,...].tolist(),
        "left_foot": pose[:,2,...].tolist(),
        "left_wrist": pose[:,3,...].tolist(),
        "left_hip": pose[:,4,...].tolist(),
        "left_knee": pose[:,5,...].tolist(),
        "left_shoulder": pose[:,6,...].tolist(),
        "neck": pose[:,7,...].tolist(),
        "right_elbow": pose[:,8,...].tolist(),
        "right_foot": pose[:,9,...].tolist(),
        "right_wrist": pose[:,10,...].tolist(),
        "right_hip": pose[:,11,...].tolist(),
        "right_knee": pose[:,12,...].tolist(),
        "right_shoulder": pose[:,13,...].tolist(),
        "torso": pose[:,14,...].tolist()
    }
    return keyframes

# pipeline entry point
def pipeline2json(video_path, out_path):
    cap = cv2.VideoCapture(video_path)
    shot_analysis = analyse_video(cap)
    cap.release()
    shots_json = {
        "shots": 
        [
            {
                "start_frame_idx": int(start_t),
                "end_frame_idx": int(end_t),
                "classification": classification,
                "world_keyframes": pose2keyframes(world_pose_frames),
                "image_pose_frames": image_pose_frames.tolist()
            } for ((start_t, end_t), classification, world_pose_frames, image_pose_frames) 
            in zip(
                shot_analysis["intervals"], 
                shot_analysis["classifications"], 
                shot_analysis["world_poses"], 
                shot_analysis["image_poses"]
            )
        ]
    }
    json.dump(shots_json, open(out_path, "w"), indent=2)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("incorrect number of arguments.")
    else:
        pipeline2json(args[0], args[1])