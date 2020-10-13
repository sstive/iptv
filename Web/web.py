import os
from flask import Flask, Response, render_template, send_from_directory
from DBHelper import Database
from Utils.db_functions import FUNCS
from Utils.generator import generate_playlist


app = Flask(__name__, static_folder='files')

db = Database('../Config/Database.json', functions=FUNCS)
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
        return Response(playlist, mimetype='text/m3u8', headers={'Content-disposition': 'attachment; filename=playlist.m3u8'})
    else:
        return "Not found", 404
# ================= #


# ----- Pages ----- #
# Login
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
    }

    if table not in tables.keys():
        return 'Not found', 404

    db.begin()
    data = db.select(table, '*')
    db.end()

    return render_template('table.html', data=data, columns=tables[table])
# ============================ #


# ----- Adding values ----- #
@app.route('/add_playlist', methods=['GET'])
def add_playlist():
    return 'dev'
# ========================= #


if __name__ == '__main__':
    app.run()
