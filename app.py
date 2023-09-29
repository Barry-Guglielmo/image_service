import os
from io import BytesIO
import io
import requests
from threading import Semaphore
import sqlite3
from flask import Flask, abort, send_file, request, send_file,render_template, make_response
from config import *



app = Flask(__name__)
state = {}

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    form = request.form
    # If the user does not select a file, the browser submits an empty part without filename
    if file.filename == '':
        return "No selected file"
    if form['first'] == '':
        return "No first level defined"
    if form['second'] == '':
        return "No second level defined"


    if file:
        file_name = file.filename
        file_data = sqlite3.Binary(file.read())
        first = request.form['first']
        second =request.form['second']

        # Save the image to the database as a stream
        conn = sqlite3.connect(IMAGE_DB)
        c = conn.cursor()
        c.execute("INSERT INTO images (first, second, file_name, image_data) VALUES (?, ?, ?, ?)", (first, second, file_name, file_data))
        conn.commit()
        conn.close()

        return f"File '{file_name}' uploaded successfully"

    return "Invalid file type"

@app.route('/<string:first>/<string:second>/<string:file_name>')
def serve_image_from_db(first, second, file_name):
    # Retrieve image data from the IMAGE_DB
    conn = sqlite3.connect(IMAGE_DB)
    c = conn.cursor()
    c.execute("SELECT first, second, file_name, image_data FROM images WHERE (first=? AND second=? AND file_name=?)", (first, second, file_name))
    result = c.fetchone()
    conn.close()

    if result:
        frist, second, file_name, image_data = result
        return send_file(
            io.BytesIO(image_data),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name=file_name
        )
    else:
        return "Image not found"

@app.route('/check/<string:first>/<string:second>/<string:file_name>')
def check_if_image_in__db(first, second, file_name):
    # Retrieve image data from the IMAGE_DB
    conn = sqlite3.connect(IMAGE_DB)
    c = conn.cursor()
    c.execute("SELECT first, second, file_name, image_data FROM images WHERE (first=? AND second=? AND file_name=?)", (first, second, file_name))
    result = c.fetchone()
    conn.close()

    if result:
        response = make_response('True')
        response.headers['Content-Type'] = 'text/plain'
        return response
    else:
        response = make_response('False')
        response.headers['Content-Type'] = 'text/plain'
        return response

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
