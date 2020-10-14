from datetime import datetime, timedelta
from Classes.channel import Channel
from DBHelper import Database
from Config.variables import THEMES


# Themes #
def themes_get(db: Database):
    """
    Function for getting themes from database
    :return: List with themes, where index = theme id
    """
    resp = db.select('themes', '*')
    themes = []

    for theme in resp:
        while len(themes) < theme[0]+1:
            themes.append(None)
        themes[theme[0]] = theme[1]

    return themes


def themes_add(db: Database, **kwargs):
    """
    Function that add new theme to database
    :key theme: name of theme, should be str
    :return: id of added theme
    """
    return db.insert_or_update('themes', name=kwargs['theme'], _return_id=True)


def themes_add_default(db: Database):
    themes = list(THEMES['themes'].keys())
    for name in themes:
        if name != '':
            db.insert_or_update('themes', id=themes.index(name), name=name)
# ------ #


# Channels #
def channels_get(db: Database):
    """
    Function for getting channels from database
    :return: List with channels
    """
    resp = db.select('channels', '*', "ORDER BY id")
    channels = []

    for db_channel in resp:
        channels.append(Channel(*db_channel))
    return channels


def channels_save(db: Database, **kwargs):
    """
    Function for saving channels to database
    :key channels: List with channels, should be list
    """
    done = 0
    for ch in kwargs['channels']:
        # TODO: Remake with single request
        done += 1
        print(f"\r\t- Saving channels... \t{done}/{len(kwargs['channels'])}", end='')
        db.insert_or_update('channels', **ch.get_dict())
    print(f"\r\t- Saving channels... Done!")
# -------- #


# Sources #
def sources_get(db: Database):
    """
    Function for getting sources from database
    :return: List with dicts of sources
    """
    resp = db.select('sources', '*')
    sources = []

    for source in resp:
        sources.append({
            'id': source[0],
            'url': source[1],
            'last_online': source[2],
            'count': source[3]
        })

    return sources


def sources_save(db: Database, **kwargs):
    """
    function for saving sources
    :key sources: List with sources
    """
    for src in kwargs['sources']:
        db.insert_or_update('sources', **src)
# ------- #


# Tasks #
def tasks_executed(db: Database, **kwargs):
    """
    Function for changing task's executing time
    :key tid: Task id
    """
    db.insert_or_update('tasks', id=kwargs['tid'], last_execution=datetime.today().date().strftime("%Y-%m-%d"), crashed=kwargs['crashed'])
# ----- #


FUNCS = {
    # Themes
    'themes.get': themes_get,
    'themes.add': themes_add,
    'themes.add_default': themes_add_default,
    # Channels
    'channels.get': channels_get,
    'channels.save': channels_save,
    # Sources
    'sources.get': sources_get,
    'sources.save': sources_save,
    # Tasks
    'tasks.executed': tasks_executed
}
