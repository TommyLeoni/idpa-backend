import os

import flask
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

from senti import analyze_text
from model.response_encoder import ResponseEncoder

SECRET_KEY = os.urandom(24)
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSION = {'txt'}

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
cors = CORS(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@app.route('/api/test', methods=['GET'])
@cross_origin()
def test():
    return "<h3>This is just the index of my backend. Nothing special to see here. </h3>" \
           "<p>Please visit https://www.idpa-tomaso.herokuapp.com to view my application. </p>"


@app.route('/api/textRawUpload', methods=['POST'])
@cross_origin()
def text_raw_upload():
    data = request.get_json()
    results = analyze_text(data['content'])
    return jsonify(results, data['content'])


@app.route('/api/textFileUpload', methods=['GET', 'POST'])
@cross_origin()
def text_file_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file in request"

        file = request.files['file']
        if file.filename == '':
            return "No file in request"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(LOCAL_PATH, filename))
            f = open(os.path.join("uploads", filename), "r", encoding="utf-8")
            file_content = f.read()
            results = analyze_text(file_content)
            return jsonify(results, file_content)


if __name__ == '__main__':
    app.run(port=5000, threaded=True)
