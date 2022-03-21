from fileinput import filename
from flask import Flask, request, render_template, redirect, url_for
import os
import json
from utilities import ANALYSIS_FOLDER, ALLOWED_EXTENSIONS
from analysis_pipeline.video_analysis import analyse_video
import hashlib
import time


app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['SHOT_ANALYSIS'] = ANALYSIS_FOLDER

app.debug = False


def allowed_file(file_name: str):
    return '.' in file_name and \
        file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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

        return redirect(f"/{analysis_id}/")
    return redirect(url_for("home"))


def view_shots(analysis_id: str, class_filter: str):
    json_path = os.path.join(app.config['SHOT_ANALYSIS'], analysis_id, "shot_analysis.json")
    with open(json_path) as json_file:
        shot_analysis = json.load(json_file)
    shots = []
    classes = set()
    if class_filter != "all":
        classes.add("all")
    for i in range(len(shot_analysis["shots"])):
        shot = shot_analysis["shots"][i]
        classification = shot["classification"]
        if classification != class_filter:
            classes.add(classification)
        if class_filter != "all" and classification != class_filter:
            continue
        clip_path = f"analysis_results/{analysis_id}/{i}{classification}.mp4"
        url = url_for('static', filename=clip_path)
        shots.append((classification, url))
    annotated_vid_path = f"analysis_results/{analysis_id}/annotated_video.mp4"
    classes = list(classes)
    classes.sort()
    return render_template("shots_dashboard.html", shots=shots, annotated_vid_url=url_for('static', filename=annotated_vid_path), classes=classes, filter=class_filter, analysis_id=analysis_id)


@app.route("/<analysis_id>", methods=["GET"])
def view_analysis(analysis_id: str):
    return view_shots(analysis_id, "all")


@app.route("/<analysis_id>/<class_filter>", methods=["GET"])
def view_filtered_analysis(analysis_id: str, class_filter: str):
    if class_filter not in ["forehand", "backhand", "smash", "service"]:
        return redirect(url_for("view_analysis", analysis_id=analysis_id))
    return view_shots(analysis_id, class_filter)


@app.route("/get_analysis?id=<analysis_id>?filter=<class_filter>", methods=["GET"])
def get_filtered_analysis_json(analysis_id: str, class_filter: str):
    json_path = os.path.join(app.config['SHOT_ANALYSIS'], analysis_id, "shot_analysis.json")
    with open(json_path) as json_file:
        shot_analysis = json.load(json_file)
    if class_filter not in ["forehand", "backhand", "smash", "service"]:
        return shot_analysis
    for i in range(len(shot_analysis['shots'])):
        if shot_analysis['shots'][i]['classification'] != class_filter:
            shot_analysis['shots'].pop(i)
    return shot_analysis


@app.route("/get_analysis?id=<analysis_id>")
def get_analysis_json(analysis_id: str):
    return get_filtered_analysis_json(analysis_id, "all")


if __name__ == '__main__':
    app.run()
