from flask import Flask, request, render_template, redirect, url_for, flash
import os
import json
from utilities.frame_extraction import create_images

#from analysis_pipeline.json_writer import pipeline2json

DATA_FOLDER = 'data/'
ALLOWED_EXTENSIONS = {'mp4'}

app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['UPLOAD FOLDER'] = DATA_FOLDER + 'videos'
app.config['SHOT ANALYSIS'] = DATA_FOLDER + 'analysis_results'

# Maybe add redirect codes if possible
# Commented out pipeline code since it doesn't run on my computer


@app.route('/display/<filename>')
def display_img(filename: str):
    return redirect(url_for('static', filename='images/' + str(filename)))


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
            json_path: str = os.path.join(app.config['SHOT ANALYSIS'], 'test_shot.json')
            file_path: str = os.path.join(app.config['UPLOAD FOLDER'], file.filename)
            file.save(file_path)
            #  pipeline2json(file_path, json_path)
            create_images(json_path, file_path)
            return redirect(url_for('send_shots', json_path=json_path))
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


@app.route("/shots_dashboard/<path:json_path>", methods=["GET", "POST"])   # I think I can change the path route?
def send_shots(json_path: str):
    with open(json_path) as json_file:
        json_dict: dict = json.load(json_file)
        shots: list = json_dict.get('shots')
    shot_classes: dict = get_classes(shots)
    shown_classes: list = get_shown_classes(request, shot_classes)
    return render_template(
        'shots_dashboard.html',
        file_name=json_path,
        shots=shots,
        shot_classes=shot_classes,
        shown_classes=shown_classes
    )


if __name__ == '__main__':
    app.run()
