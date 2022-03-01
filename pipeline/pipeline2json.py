import cv2
import json
import sys
import numpy
from analyse_video import analyse_video

def pipeline2json(video_path, out_path):
    cap = cv2.VideoCapture(video_path)
    shot_frames, shot_classifications = analyse_video(cap)
    shots_json = {
        "shots": [{"classification": c, "frames": f.tolist()} for (c, f) in zip(shot_classifications, shot_frames)]
    }
    json.dump(shots_json, open(out_path, "w"))

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("incorrect number of arguments.")
    else:
        pipeline2json(args[0], args[1])