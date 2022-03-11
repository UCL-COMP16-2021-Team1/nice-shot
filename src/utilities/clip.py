# CREATES VIDEO CLIPS
import cv2
from os.path import isdir, join
from os import mkdir
# from . import DATA_FOLDER, VIDEO_FOLDER
from .constants import STATIC_VIDEOS
import json


DATA_FOLDER: str = 'static'
VIDEO_FOLDER: str = join('static', 'videos')


def create_video_folder():
    if not isdir(DATA_FOLDER):
        mkdir(DATA_FOLDER)


def trim_video(data, cam, shot_index: int) -> list:
    global VIDEO_FOLDER
    current_frame_count: int = 0
    shot = data['shots'][shot_index]
    frames = []
    while True:
        _, frame = cam.read()
        if shot['start_frame_idx'] <= current_frame_count <= shot['end_frame_idx']:
            frames.append(frame)
        elif current_frame_count > shot['end_frame_idx']:
            break
        current_frame_count += 1
    return frames


def create_video(out_video: str, frames: list, cam):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cam.get(cv2.CAP_PROP_FPS))
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_writer = cv2.VideoWriter(out_video, fourcc, fps, (width, height))
    for frame in frames:
        video_writer.write(frame)
    video_writer.release()


def create_clip(json_filename: str, shot_index: int, video_dir: str):
    create_video_folder()
    with open(json_filename) as file:
        data = json.load(file)
        cam = cv2.VideoCapture(video_dir)
        frames = trim_video(data, cam, shot_index)
        create_video(join(STATIC_VIDEOS, f'clip{shot_index}.mp4'), frames, cam)
        cam.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    create_clip('data/analysis_results/test_shot.json', 0, 'data/videos/p1_backhand_s1.mp4')
