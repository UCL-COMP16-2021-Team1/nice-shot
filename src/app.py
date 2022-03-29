import shutil
from flask import Flask, request, render_template, redirect, url_for, abort
import os
import json

from utilities import ANALYSIS_FOLDER, ALLOWED_EXTENSIONS
from analysis_pipeline.video_analysis import AnalysisFailedError, analyse_video
import hashlib
import time
from multiprocessing import Process


app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['SHOT_ANALYSIS'] = ANALYSIS_FOLDER

app.debug = False


def allowed_file(file_name: str):
    return '.' in file_name and \
        file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


def render_error(error_message: str):
    return render_template("error.html", error_message=error_message)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_error("No video file received.")
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return render_error("Invalid video filename. Supported extensions include .mp4, .mov, and .avi.")

        hasher = hashlib.sha1(str(file.filename).encode('utf-8') + str(time.time()).encode('utf-8'))
        analysis_id = str(hasher.hexdigest()[:10])
        analysis_dir = os.path.join(app.config['SHOT_ANALYSIS'], analysis_id)
        os.mkdir(analysis_dir)
        video_path = os.path.join(analysis_dir, f"{analysis_id}_{file.filename}")
        file.save(video_path)

        try:
            analyse_video(video_path, analysis_dir)
            os.remove(video_path)
        except AnalysisFailedError as e:
            os.remove(video_path)
            os.rmdir(analysis_dir)
            return render_error(str(e))

        return redirect(f"/{analysis_id}")
    return redirect(url_for("home"))


def analysis_exits(analysis_id: str):
    if os.path.isdir(os.path.join(app.config['SHOT_ANALYSIS'], analysis_id)):
        return True
    return False


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
        speed = shot["speed"] * shot_analysis["fps"]
        speed = round(speed, 3)
        hand = shot["hand"]
        duration = (shot["end_frame_idx"] - shot["start_frame_idx"]) / shot_analysis["fps"]
        duration = round(duration, 1)
        clip_path = f"analysis_results/{analysis_id}/{i}{classification}.mp4"
        clip_url = url_for('static', filename=clip_path)

        bvh_path = f"analysis_results/{analysis_id}/{i}{classification}.bvh"
        bvh_url = url_for('static', filename=bvh_path)
        shots.append((classification, clip_url, speed, hand, duration, bvh_url))
    annotated_vid_path = f"analysis_results/{analysis_id}/annotated_video.mp4"
    classes = list(classes)
    classes.sort()
    return render_template("shots_dashboard.html", shots=shots, annotated_vid_url=url_for('static', filename=annotated_vid_path), classes=classes, filter=class_filter, analysis_id=analysis_id)


@app.route("/<analysis_id>", methods=["GET"])
def view_analysis(analysis_id: str):
    if not analysis_exits(analysis_id):
        return render_error("404 analysis not found")
    return view_shots(analysis_id, "all")


@app.route("/<analysis_id>/<class_filter>", methods=["GET"])
def view_filtered_analysis(analysis_id: str, class_filter: str):
    if not analysis_exits(analysis_id):
        return render_error("404 analysis not found")
    if class_filter not in ["forehand", "backhand", "smash", "service"]:
        return redirect(url_for("view_analysis", analysis_id=analysis_id))
    return view_shots(analysis_id, class_filter)


@app.route("/<analysis_id>/<class_filter>/get_analysis", methods=["GET"])
def get_filtered_analysis_json(analysis_id: str, class_filter: str):
    if not analysis_exits(analysis_id):
        return render_error("404 analysis not found")
    json_path = os.path.join(app.config['SHOT_ANALYSIS'], analysis_id, "shot_analysis.json")
    with open(json_path) as json_file:
        shot_analysis = json.load(json_file)
    if class_filter not in ["forehand", "backhand", "smash", "service"]:
        return shot_analysis
    i = 0
    while i < len(shot_analysis['shots']):
        if shot_analysis['shots'][i]['classification'] != class_filter:
            shot_analysis['shots'].pop(i)
        else:
            i += 1
    return shot_analysis


@app.route("/<analysis_id>/get_analysis")
def get_analysis_json(analysis_id: str):
    return get_filtered_analysis_json(analysis_id, "all")


@app.route("/<analysis_id>/3d/<int:index>", methods=["GET"])
def view_3d_analysis(analysis_id: str, index: int):
    if not analysis_exits(analysis_id):
        return render_error("404 analysis not found")
    return render_template("3d.html", analysis_url=url_for("get_analysis_json", analysis_id=analysis_id), shot_index=index)


@app.route("/<analysis_id>/<class_filter>/3d/<int:index>", methods=["GET"])
def view_filtered_3d_analysis(analysis_id: str, class_filter: str, index: int):
    if not analysis_exits(analysis_id):
        return render_error("404 analysis not found")
    if class_filter not in ["forehand", "backhand", "smash", "service"]:
        return redirect(url_for("view_3d_analysis", analysis_id=analysis_id, index=index))
    return render_template("3d.html", analysis_url=url_for("get_filtered_analysis_json", analysis_id=analysis_id, class_filter=class_filter), shot_index=index)


def delete_old_analysis():
    while True:
        ids = [d.name for d in os.scandir(app.config["SHOT_ANALYSIS"]) if d.is_dir()]
        for i in ids:
            if i == "example":
                continue
            json_path = os.path.join(app.config['SHOT_ANALYSIS'], i, "shot_analysis.json")
            if not os.path.isfile(json_path):   # analysis still processing
                continue
            now = time.time()
            if os.stat(json_path).st_mtime < now - 86400:
                shutil.rmtree(os.path.join(app.config['SHOT_ANALYSIS'], i))
        time.sleep(60)


if __name__ == '__main__':
    p = Process(target=delete_old_analysis)
    p.start()
    app.run()
    p.join()
