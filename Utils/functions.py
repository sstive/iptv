from datetime import datetime, timedelta

from Classes.channel import Channel
from DBHelper import Database


# Channels #
def channels_get(db: Database, **kwargs):
    """
    Function for getting channels from database
    :return: List with channels
    """
    resp = db.select('channels', '*')
    channels = []

    for db_channel in resp:
        channels.append(
            Channel(
                id=db_channel[0],
                name=db_channel[1],
                theme=db_channel[2],
                urls=db_channel[3],
                online=db_channel[4],
                source_id=db_channel[5]
            )
        )
    return channels


def channels_save(db: Database, **kwargs):
    """
    Function for saving channels to database
    :key channels: List with channels, should be list
    """
    # request = ""

    done = 0
    for ch in kwargs['channels']:
        # TODO: Add one request
        done += 1
        print(f"\r\t- Saving channels... \t{done}/{len(kwargs['channels'])}", end='')
        db.insert_or_update('channels', **ch.get_dict())

        """values = ch.get_dict()
        values['_request'] = True
        request += db.insert_or_update('channels', **values)

        if done % 5:
            # Progress
            done += 5
            print(f"\r\t- Saving channels... \t{done}/{len(kwargs['channels'])}", end='')

            print(request)
            db.execute(request)
            request = ""
        """

    # if request != "":
    #     db.execute(request)

# -------- #


# Sources #
def sources_get(db: Database, **kwargs):
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
def tasks_get_date(db: Database, **kwargs):
    """
    Function for getting task from database
    :key tid: Task id
    :return: Datetime when task should be executed
    """
    resp = db.select('tasks', ['execute_after'], f"WHERE id={kwargs['tid']}")
    if len(resp) == 0:
        return datetime.now().date()
    return resp[0][0]


def tasks_prolong(db: Database, **kwargs):
    """
    Function for changing task's executing time
    :key tid: Task id
    """
    next_time = datetime.today() + timedelta(days=1)
    db.insert_or_update('tasks', id=kwargs['tid'], execute_after=next_time.date().strftime("%Y-%m-%d"))
# ----- #


FUNCS = {
    'channels.get': channels_get,
    'channels.save': channels_save,
    'sources.get': sources_get,
    'sources.save': sources_save,
    'tasks.get_date': tasks_get_date,
    'tasks.prolong': tasks_prolong
}
