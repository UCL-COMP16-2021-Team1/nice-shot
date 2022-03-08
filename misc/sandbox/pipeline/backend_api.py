from fileinput import filename
from pipeline2json import pipeline2json
from flask import Flask, request, flash, redirect, render_template, url_for
import os



UPLOAD_FOLDER = 'videofiles'
ALLOWED_EXTENSIONS = {'mp4'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file'not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            jsonPath = "test.json"
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filePath)
            pipeline2json(filePath, jsonPath)
            return redirect(url_for("viewVideo", jsonpath=jsonPath))
    return render_template("upload.html")

@app.route('/view/<jsonpath>')
def viewVideo(jsonpath):
    # just directs to html page that displays the json file name
    return render_template("viewjson.html", jsonName=jsonpath)

if __name__ == "__main__":
    app.run()