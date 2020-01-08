import os.path
from flask import Flask, send_from_directory, request

app = Flask(__name__)


@app.route('/playlist')
def get_playlist():
    pl = 'default.m3u8'
    if request.args.get('pl'):
        pl = request.args.get('pl') + '.m3u8'
        if not os.path.isfile(pl):
            pl = 'default.m3u8'
    return send_from_directory(directory='playlists', filename=pl)
