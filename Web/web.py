from flask import Flask, Response
from Utils.generator import generate_playlist


app = Flask(__name__)


# --- Playlists --- #
@app.route('/p/<pl_id>')
def get_playlist(pl_id):
    playlist = generate_playlist(int(pl_id))
    if playlist is not None:
        return Response('\n'.join(playlist), mimetype='text/m3u8', headers={'Content-disposition': 'attachment; filename=playlist.m3u8'})
    else:
        return "Not found", 404
# ================= #


# ----- Pages ----- #
@app.route('/')
def index():
    # Todo: make page
    return 'Index'


@app.route('/login')
def login():
    # Todo: make page
    return 'Login'
# ================= #


if __name__ == '__main__':
    app.run()
