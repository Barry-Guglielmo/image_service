import os
from io import BytesIO
import requests
from threading import Semaphore
from flask import Flask, abort, send_file, request

from cache import PlotCache

PLOTS_DATABASE = os.path.abspath('plots.db')

app = Flask(__name__)
state = {}

plot_cache = PlotCache(PLOTS_DATABASE)

@app.route('/livedesign/image_service/', methods=['GET'])
def image_service():
    return app.send_static_file('test.html')

'''
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
