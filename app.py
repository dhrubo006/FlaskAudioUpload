
from email.mime import audio
from flask import Flask, render_template, redirect, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB
app.config['ALLOWED_EXTENSIONS'] = ['.wav', '.mp3', '.aac', '.ogg', '.flac']


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_DIRECTORY'])
    audio_files = []

    for file in files:
        if os.path.splitext(file)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
            audio_files.append(file)

    return render_template('index.html', audio_files=audio_files)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']

        if file:
            extension = os.path.splitext(file.filename)[1].lower()

            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return 'File is not an audio.'

            file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(file.filename)
            ))

    except RequestEntityTooLarge:
        return 'File is larger than the 200MB limit.'

    return redirect('/')


@app.route('/play_audio/<filename>', methods=['GET'])
def play_audio(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)


if __name__== '__main__':
  app.run(debug = True)
