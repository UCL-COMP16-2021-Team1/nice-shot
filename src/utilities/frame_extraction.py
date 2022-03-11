import cv2
import json
from os.path import isdir, join
from os import mkdir
from .constants import DATA_FOLDER, STATIC_IMAGES


def create_image_folder():
    if not isdir(DATA_FOLDER):
        mkdir(DATA_FOLDER)


def analyse_frames(data: dict, cam):
    global STATIC_IMAGES
    current_frame: int = 0
    shot_count: int = 0
    for shot in data['shots']:
        while True:
            _, frame = cam.read()
            if current_frame == shot['start_frame_idx']:
                img_name = join(STATIC_IMAGES, f"clip{shot_count}.jpg")
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
