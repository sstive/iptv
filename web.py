from os import environ as env
from flask import Flask, Response, render_template, request, redirect
from DBHelper import Database
from Utils.db_functions import FUNCS
from Utils.generator import generate_playlist

app = Flask(__name__, static_folder='Web/files', template_folder='Web/templates')

db = Database('Config/Database.json', functions=FUNCS)
db.end()


# --- Playlists --- #
@app.route('/p/<pl_id>')
def get_playlist(pl_id):
    try:
        pl_id = int(pl_id)
    except ValueError:
        return "Bad id", 400

    db.begin()
    playlist = generate_playlist(pl_id, db)
    db.end()

    if playlist is not None:
        return Response(playlist, mimetype='text/m3u8',
                        headers={'Content-disposition': 'attachment; filename=playlist.m3u8'})
    else:
        return "Not found", 404


# ================= #


# ----- Pages ----- #
# TODO: make authorization
@app.route('/')
def index():
    return render_template("login.html", fail=False)


@app.route('/', methods=['POST'])
def login():
    return render_template("login.html", fail=True)


# ================= #


# ----- Database showing ----- #
@app.route('/database')
def database():
    return render_template('database.html')


@app.route('/database/<table>')
def db_tables(table):
    tables = {
        'channels': [
            {'name': "Name", 'index': 1},
            {'name': "Id", 'index': 0},
            {'name': "Theme", 'index': 2},
            {'name': "Source id", 'index': 5}
        ],
        'sources': [
            {'name': "ID", 'index': 0},
            {'name': "URL", 'index': 1},
            {'name': "Last online", 'index': 2},
            {'name': "Count", 'index': 3}
        ],
        'themes': [
            {'name': "ID", 'index': 0},
            {'name': "Name", 'index': 1}
        ],
        'playlists': [
            {'name': "ID", 'index': 0},
            {'name': "Quality", 'index': 1},
            {'name': "Channels", 'index': 2},
            {'name': "Delete", 'index': 3}
        ],
        'tasks': [
            {'name': "ID", 'index': 0},
            {'name': "Last execution", 'index': 1},
            {'name': "Error", 'index': 2}
        ],
    }

    if table not in tables.keys():
        return 'Not found', 404

    db.begin()
    data = db.select(table, '*')
    db.end()

    return render_template('table.html', data=data, columns=tables[table])


# ============================ #


# ----- Adding values ----- #
@app.route('/add')
def add_values():
    return render_template('adding.html')


@app.route('/add_playlist', methods=['POST'])
def add_playlist():
    if 'token' not in request.form.keys() or request.form.get('token') != env['TOKEN']:
        return 'Not allowed', 403

    if 'quality' not in request.form.keys() or 'channels' not in request.form.keys():
        return 'not enough args! (needs quality, channels, delete)', 400

    db.begin()
    db.insert(
        'playlists',
        quality=int(request.form['quality']),
        channels=request.form['channels'].replace(' ', ''),
        del_channels=('del_channels' in request.form.keys())
    )
    db.end()

    return redirect("/database/playlists")


@app.route('/add_source', methods=['POST'])
def add_source():
    if 'token' not in request.form.keys() or request.form['token'] != env['TOKEN']:
        return 'Not allowed', 403

    if 'url' not in request.form.keys():
        return 'not enough args! (needs url)', 400

    db.begin()
    db.insert(
        'sources',
        url=request.form['url'],
    )
    db.end()

    return redirect("/database/sources")


# ========================= #


if __name__ == '__main__':
    app.run()
