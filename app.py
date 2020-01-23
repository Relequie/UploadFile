# https://github.com/Relequie/UploadFile
from flask import Flask, redirect, url_for, render_template, flash, request, abort, send_file, send_from_directory
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return redirect(url_for('display_all_files'))

@app.route('/display_all_files/')
def display_all_files():
    files = []
    for r, d, f in os.walk(UPLOAD_FOLDER):
        for file in f:
            files.append(file)
    return render_template('display.html', files=files)

@app.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('display_all_files'))
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('display_all_files'))

@app.route('/rename/<filename>')
def rename_file(filename, newname):
    os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], newname))
    return redirect(url_for('display_all_files'))

if __name__ == '__main__':
    app.run(debug=True)