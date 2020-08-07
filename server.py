import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

import spacy
from spacy_langdetect import LanguageDetector
from components.analysis.german_analysis import analyze_german
from components.analysis.english_analysis import analyze_english

# Setup nlp for language detection
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

# Basic local variables for file transfer
SECRET_KEY = os.urandom(24)
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSION = {'txt'}

# Setup flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
cors = CORS(app)
app.debug = True


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@app.route('/api/test', methods=['GET'])
@cross_origin()
def test():
    return "<h3>This is just the index of the backend. Nothing special to see here. </h3>" \
           "<p>Please visit https://www.idpa-tomaso.herokuapp.com to view the application. </p>"


@app.route('/api/textRawUpload', methods=['POST'])
@cross_origin()
def text_raw_upload():
    # noinspection PyGlobalUndefined
    global results
    data = request.get_json()

    doc = nlp(data['content'])
    if doc._.language['language'] == 'de':
        results = analyze_german(data['content'])
    elif doc._.language['language'] == 'en':
        results = analyze_english(data['content'])

    return jsonify(results, data['content'])


# noinspection PyGlobalUndefined
@app.route('/api/textFileUpload', methods=['GET', 'POST'])
@cross_origin()
def text_file_upload():
    global raw_results
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file in request"

        file = request.files['file']
        if file.filename == '':
            return "No file in request"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(LOCAL_PATH, "uploads", filename))
            f = open(os.path.join(LOCAL_PATH, "uploads", filename), "r", encoding="utf-8")
            file_content = f.read()
            doc = nlp(file_content)

            if doc._.language['language'] == 'de':
                raw_results = analyze_german(file_content)
            elif doc._.language['language'] == 'en':
                raw_results = analyze_english(file_content)

            f.close()
            os.remove(os.path.join(LOCAL_PATH, "uploads", filename))

            return jsonify(raw_results)


if __name__ == '__main__':
    app.run(port=5000, threaded=True)
