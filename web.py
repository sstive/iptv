import os
from flask import Flask, request, render_template, Response
from werkzeug.utils import redirect
from updater.database import Database
from updater.source import Source

app = Flask(__name__, template_folder='web')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/playlist')
def get_playlist():
    db = Database(True)
    data = ''
    if request.args.get('id'):
        data = db.get_playlist(id=request.args.get('id'))
    else:
        data = db.get_playlist(id=0)
    return Response(data, mimetype='text/m3u8', headers={'Content-disposition': 'attachment; filename=playlist.m3u8'})


@app.route('/addsource', methods=['post', 'get'])
def add_source():
    message = ''
    if request.method == 'POST':
        url = request.form.get('url').replace(' ', '')
        password = request.form.get('password')

        if password == app.config['SECRET_KEY']:
            db = Database(True)
            source = Source(url=url)
            db.add_source(source)
            message = 'Success'
        else:
            message = 'Wrong password!'

    return render_template('add_source.html', message=message)


@app.route('/channel')
def channel():
    if request.args.get('id') and request.args.get('q'):
        db = Database()
        url = db.get_channel(id=request.args.get('id')).get_url(int(request.args.get('q')))
        if type(url) == int:
            return 404
        return redirect(url)
    else:
        # TODO: picture
        return 404
