import os
from io import BytesIO
import io
import requests
from threading import Semaphore
import sqlite3
from flask import Flask, abort, send_file, request, send_file,render_template
from config import *
from cache import PlotCache



app = Flask(__name__)
state = {}
plot_cache = PlotCache(IMAGE_DB)

# Function to check if an allowed file type
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def index():
#     return render_template('upload.html')

@app.route('/livedesign/images/upload', methods=['POST'])
def upload_file():
    print(request.files)
    print(request.form)

    file = request.files['file']
    form = request.form
    # If the user does not select a file, the browser submits an empty part without filename
    if file.filename == '':
        return "No selected file"
    if form['first'] == '':
        return "No first level defined"
    if form['second'] == '':
        return "No second level defined"
    


    if file and allowed_file(file.filename):
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

@app.route('/livedesign/images/<string:first>/<string:second>/<string:file_name>')
def serve_image_from_db(first, second, file_name):
    # Retrieve image data from the IMAGE_DB
    conn = sqlite3.connect(IMAGE_DB)
    c = conn.cursor()
    c.execute("SELECT first, second, file_name, image_data FROM images WHERE (first=? AND second=? AND file_name=?)", (first, second, file_name))
    result = c.fetchone()
    conn.close()

    if result:
        frist, second, file_ame, image_data = result
        return send_file(
            io.BytesIO(image_data),
            mimetype='image/jpeg',  # Adjust the mimetype as needed
            as_attachment=False,
            attachment_filename=file_name
        )
    else:
        return "Image not found"

if __name__ == '__main__':
    app.run(debug=True)

'''
# Adams Code
@app.route('/livedesign/image_service/', methods=['GET'])
def image_service():
    args = request.args.to_dict()
    vault_id = args['vault']
    batch_id = args['batch']
    protocol_id = args['protocol']

    blob = plot_cache.get(vault_id, batch_id, protocol_id)

    return send_file(BytesIO(blob),
                     mimetype='image/png',
                     as_attachment=True,
                     download_name=f'{vault_id}_{batch_id}_{protocol_id}.png')
'''
