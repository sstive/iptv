import os
import collections
from flask import Flask, request, render_template, Response, send_from_directory
from werkzeug.utils import redirect
from classes.database import Database
from classes.source import Source

app = Flask(__name__, template_folder='web')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/playlist')
def get_playlist():
    db = Database(True)
    if request.args.get('id'):
        data = db.get_playlist(id=request.args.get('id'))
    else:
        data = db.get_playlist(id=0)
    return Response(data, mimetype='text/m3u8', headers={'Content-disposition': 'attachment; filename=playlist.m3u8'})


@app.route('/addsource', methods=['post', 'get'])
def add_source():
    message = ''
    style = ''
    if request.method == 'POST':
        url = request.form.get('url').replace(' ', '')
        password = request.form.get('password')

        if password == app.config['SECRET_KEY'] and url != '':
            db = Database(True)
            source = Source(url=url)
            db.add_source(source)
            message = 'Success'
            style = 'success'
        else:
            message = 'Wrong password or URL!'
            style = 'failed'

    return render_template('add_source.html', message=message, style=style)


@app.route('/channel')
def channel():
    if request.args.get('id') and request.args.get('q'):
        db = Database(True)
        url = db.get_channel(id=request.args.get('id')).get_url(int(request.args.get('q')))
        if type(url) == int:
            return 404
        return redirect(url)
    else:
        # TODO: picture
        return 404


@app.route('/addplaylist', methods=['post', 'get'])
def add_playlist():
    message = ''
    style = ''

    db = Database(True)
    channels = db.get_channels()

    if request.method == 'POST':
        message = 'ok'
        style = 'success'
        print(request.form.getlist('selected'))

    return render_template('add_playlist.html', channels=collections.OrderedDict(sorted(channels.items())), message=message, style=style)


@app.route('/web/<path:path>')
def give_styles(path):
    return send_from_directory('web', path)
