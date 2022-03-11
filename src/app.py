from flask import Flask, request, render_template, redirect, url_for, flash
import os
import json
from utilities.frame_extraction import create_images
from utilities import create_clip, create_images
from os.path import join
from utilities import file_path, json_path, ANALYSIS_FOLDER, ALLOWED_EXTENSIONS, STATIC_VIDEOS, STATIC_IMAGES
# from analysis_pipeline.json_writer import pipeline2json


app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['SHOT ANALYSIS'] = ANALYSIS_FOLDER
app.config['STATIC VIDEOS'] = STATIC_VIDEOS
app.config['STATIC IMAGES'] = STATIC_IMAGES

app.debug = True


# Maybe add redirect codes if possible
# Commented out pipeline code since it doesn't run on my computer


@app.route('/display/<filename>')
def display_img(filename: str):
    return redirect(url_for('static', filename=f'media/images/{filename}'))


def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(request.url)
        else:
            global json_path, file_path
            json_path = os.path.join(app.config['SHOT ANALYSIS'], 'test_shot.json')
            file_path = os.path.join(app.config['STATIC VIDEOS'], f'{file.filename}')
            file.save(file_path)
            #  pipeline2json(file_path, json_path)
            create_images(json_path, file_path)
            return redirect(url_for('send_shots'))
    return render_template("index.html")


def get_classes(shots: list) -> dict:
    classes: dict = {}
    for index in range(len(shots)):
        if classes.get(shots[index]['classification']) is None:
            classes[shots[index]['classification']] = 1
        else:
            classes[shots[index]['classification']] += 1
    return classes


def get_shown_classes(class_request, shot_classes) -> list:
    if class_request.method == "POST":
        shown_classes: list = class_request.form.getlist("classCB")
    else:
        shown_classes: list = list(shot_classes.keys())
    return shown_classes


@app.route("/shots_dashboard/", methods=["GET", "POST"])  # I think I can change the path route?
def send_shots():
    global json_path
    with open(json_path) as json_file:
        json_dict: dict = json.load(json_file)
        shots: list = json_dict.get('shots')
    shot_classes: dict = get_classes(shots)
    shown_classes: list = get_shown_classes(request, shot_classes)
    return render_template(
        'shots_dashboard.html',
        shots=shots,
        shot_classes=shot_classes,
        shown_classes=shown_classes
    )


@app.route("/shot/video/<int:index>", methods=['GET', 'POST'])
def view_shot_video(index: int):
    with open(json_path) as json_file:
        json_dict: dict = json.load(json_file)
        classification: str = json_dict.get('shots')[index].get('classification')
    create_clip(json_path, index, file_path)
    return render_template("video.html", threeD=False, clip_index=(index+1), shot_class=classification, video_url=url_for('static', filename=f'media/videos/clip{index}.mp4'))


@app.route("/shot/3D/<int:index>", methods=['GET', 'POST'])
def view3d(index: int):
    index: int = index-1
    with open(json_path) as json_file:
        json_dict: dict = json.load(json_file)
        shot_data: dict = json_dict['shots'][index]
    return render_template("3d.html", shot_data=shot_data)


if __name__ == '__main__':
    app.run()
