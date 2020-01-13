import os
from flask import Flask, send_from_directory, request, render_template
from updater.database import Database
from updater.source import Source


app = Flask(__name__, template_folder='web')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/playlist')
def get_playlist():
    pl = 'default.m3u8'
    if request.args.get('pl'):
        pl = request.args.get('pl') + '.m3u8'
        if not os.path.isfile(pl):
            pl = 'default.m3u8'
    return send_from_directory(directory='playlists', filename=pl)


@app.route('/addsource', methods=['post', 'get'])
def add_source():
    message = ''
    if request.method == 'POST':
        url = request.form.get('url').replace(' ', '')
        password = request.form.get('password')

        if password == app.config['SECRET_KEY']:
            db = Database()
            source = Source(url=url)
            db.add_source(source)
            message = 'Success'
        else:
            message = 'Wrong password!'

    return render_template('add_source.html', message=message)


@app.route('/channel')
def channel():
    pass
