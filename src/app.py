from flask import Flask, request, render_template, redirect, url_for
import os
import json
from utilities import ANALYSIS_FOLDER, ALLOWED_EXTENSIONS
from analysis_pipeline.video_analysis import analyse_video
import hashlib
import time


app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['SHOT_ANALYSIS'] = ANALYSIS_FOLDER

app.debug = True


def allowed_file(file_name: str):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            return redirect(url_for("home"))
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(url_for("home"))

        hasher = hashlib.sha1(str(file.filename).encode('utf-8') + str(time.time()).encode('utf-8'))
        analysis_id = str(hasher.hexdigest()[:10])
        analysis_dir = os.path.join(app.config['SHOT_ANALYSIS'], analysis_id)
        os.mkdir(analysis_dir)
        video_path = os.path.join(analysis_dir, file.filename)
        file.save(video_path)

        analyse_video(video_path, analysis_dir)
        os.remove(video_path)

        #return redirect(f"/{analysis_id}/")
        redirect(url_for("home"))
    return redirect(url_for("home"))

"""
def get_classes(shots: list) -> dict:
    classes: dict = {}
    for index in range(len(shots)):
        if classes.get(shots[index]['classification']) is None:
            classes[shots[index]['classification']] = 1
        else:
            classes[shots[index]['classification']] += 1
    return classes


@app.route("/<analysis_id>/", methods=["GET", "POST"])
def send_shots(analysis_id: str):
    json_path = os.path.join(app.config['SHOT_ANALYSIS'], analysis_id, "shot_analysis.json")
    with open(json_path) as json_file:
        json_dict: dict = json.load(json_file)
        shots: list = json_dict.get('shots')
    shot_classes: dict = get_classes(shots)
    shown_classes: list = list(shot_classes.keys())
    return render_template(
        'shots_dashboard.html',
        shots=shots,
        shot_classes=shot_classes,
        shown_classes=shown_classes
    )


@app.route("/<analysis_id>/view?index=<int:index>", methods=['GET', 'POST'])
def view_shot_video(analysis_id: str, index: int):
    json_path = os.path.join(app.config['SHOT ANALYSIS'], analysis_id, "shot_analysis.json")
    video_path = os.path.join(app.config['SHOT ANALYSIS'], analysis_id, "annotated_video.mp4")
    with open(json_path) as json_file:
        json_dict: dict = json.load(json_file)
        classification: str = json_dict.get('shots')[index].get('classification')
    create_clip(json_path, index, file_path)
    return render_template("video.html", threeD=False, clip_index=(index+1), shot_class=classification, video_url=url_for(filename=file_path))


@app.route("/<analysis_id>/shot/3D/<int:index>", methods=['GET', 'POST'])
def view3d(analysis_id: str, index: int):
    json_path = os.path.join(app.config['SHOT ANALYSIS'], analysis_id, "shot_analysis.json")
    index: int = index-1
    with open(json_path) as json_file:
        json_dict: dict = json.load(json_file)
        shot_data: dict = json_dict['shots'][index]
    return render_template("3d.html", shot_data=shot_data)
"""

if __name__ == '__main__':
    app.run()
