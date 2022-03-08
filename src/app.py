from flask import Flask, request, flash, redirect, make_response, Response, render_template, redirect, url_for
import os
import json

app = Flask(__name__, template_folder='ui/templates', static_folder='ui')
app.config['UPLOAD_FOLDER'] = 'data'


# what are these redirect codes?
@app.route('/', methods=['GET', 'POST'])
def get_shot_results():
    if request.method == 'POST':
        json_path = os.path.join(app.config['UPLOAD_FOLDER'], 'analysis_results/test_shot.json')
        print(json_path)
        print(f"GET SHOTS {request.method}")
        return redirect(url_for('get_shots', json_path=json_path))  # json_path=json_path))
    return render_template('index.html')


def extract_shot_data(json_file):
    json_dict: dict = json.load(json_file)
    shots: list = json_dict.get('shots')
    shot_count: int = len(shots)
    return shots, shot_count


def get_shot_dictionary(shots: list, shot_count: int) -> dict:
    # change name to shot classification dictionary
    shot_dict: dict = {}
    for i in range(shot_count):
        if shot_dict.get(shots[i]['classification']) is None:
            shot_dict[shots[i]['classification']] = 1
        else:
            shot_dict[shots[i]['classification']] += 1
    return shot_dict


def get_json_data(json_path: str):
    shots_list: list = []
    shot_count: int = 0
    with open(json_path) as json_file:
        shots_list, shot_count = extract_shot_data(json_file)
    shot_dict: dict = get_shot_dictionary(shots_list, shot_count)
    return shots_list, shot_count, shot_dict


def extract_classifications(shot_dict: dict) -> list:
    return list(shot_dict.keys())


# @app.route('shots_dashboard/<path:json_path>')
# def display_shots(json_path):
"""
PSEUDOCODE FOR SENDING OVER SHOT DATA

ROUTES:
JSON_PATH, LIST OF SHOWN CLASSIFICATIONS
for the GETTER method, list of shown classifications is not needed.

RETRIEVE DATA:
1. get list of shots (all the data in them)
2. create dictionary containing shot class information
3. get list of shown classifications IF SHOWN CLASSIFICATIONS DOES NOT EXIST YET

then send:
renderTemplate(shots_dashboard.html)
WITH:
- shot list
- shot class dictionary
- list of shown classifications

WHENEVER THE HTML FILE IS LOADED:
ONLY USE THIS DATA TO DETERMINE what should and should not appear. DO NOT DO DYNAMIC PROCESSING (i.e. does not analyse the contents of the webpage to determine variables)

"""

#@app.route('/shots_dashboard/<path:json_path>/<string:shown_classes>')


@app.route('/shots_dashboard/<path:json_path>')
def get_shots(json_path: str, shown_classes=''):
    print(json_path)
    shots_list, _, shot_classes_dict = get_json_data(json_path)
    shown_classifications: list = []
    #if request.method == 'POST':
     #   shown_classifications = shown_classes.split(',')
    #else:
    shown_classifications = extract_classifications(shot_classes_dict)
    return render_template(
        'shots_dashboard.html',
        shots_list=shots_list,
        shot_classes_dict=shot_classes_dict,
        shown_classifications=shown_classifications
    )


@app.route('/display/<filename>')  # just for showing images
def display_img(filename: str):
    return redirect(url_for('static', filename='images/' + str(filename)))


@app.route('/shots_dashboard/<path:json_path>')
def display_shots(json_path, classifications: list = None):  # , classifications: list):
    shots_list, shot_count, shot_dict = get_json_data(json_path)
    shown_classifications: list = extract_classifications(shot_dict)
    if request.method == 'POST':
        shown_classifications: list = classifications
    return render_template(
        'shots_dashboard.html',
        shots_list=shots_list,
        count=shot_count,
        shot_dict=shot_dict,  # classification dictionary
        classifications=shown_classifications,
        shown_classifications=shown_classifications
    )


if __name__ == '__main__':
    app.run()
