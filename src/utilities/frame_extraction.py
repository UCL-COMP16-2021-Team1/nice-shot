import cv2
import json
from os.path import isdir, join
from os import mkdir
from . import DATA_FOLDER, SHOT_IMAGES_FOLDER


#DATA_FOLDER = 'data'
#VIDEO_FOLDER = join(DATA_FOLDER, 'videos')
#ANALYSIS_FOLDER = join(DATA_FOLDER, 'analysis_results')
#SHOT_IMAGES_FOLDER = 'static/images'


def create_image_folder():
    if not isdir(DATA_FOLDER):
        mkdir(DATA_FOLDER)


def analyse_frames(data: dict, cam):
    global SHOT_IMAGES_FOLDER
    current_frame: int = 0
    shot_count: int = 0
    for shot in data['shots']:
        while True:
            _, frame = cam.read()
            if current_frame == shot['start_frame_idx']:
                img_name = join(SHOT_IMAGES_FOLDER, f"shot{shot_count}.jpg")
                cv2.imwrite(img_name, frame)
                current_frame += 1
                shot_count += 1
                break
            current_frame += 1


def create_images(json_filename: str, video_dir: str):
    create_image_folder()
    with open(json_filename) as file:
        data = json.load(file)
        cam = cv2.VideoCapture(video_dir)
        analyse_frames(data, cam)
        cam.release()
        cv2.destroyAllWindows()
