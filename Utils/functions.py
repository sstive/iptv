from DBHelper import Database


# Channels #
def channels_get(db: Database, **kwargs):
    """
    Function for getting channels from database
    :return: List with channels
    """
    return


def channels_save(db: Database, **kwargs):
    """
    Function for saving channels to database
    :key channels: List with channels
    """
    urls = []
    online = 0
    for q in urls:
        if len(q) > 0:
            online += 1
        online *= 2
    online //= 2
    pass
# -------- #


# Sources #
def sources_get(db: Database, **kwargs):
    """
    Function for getting sources from database
    :return: List with dicts of sources
    """
    return


def sources_save(db: Database, **kwargs):
    """
    function for saving sources
    :key sources: List with sources
    """
    pass
# ------- #


# Tasks #
def tasks_get_date(db: Database, **kwargs):
    """
    Function for getting task from database
    :key tid: Task id
    :return: Datetime when task should be executed
    """
    return


def tasks_prolong(db: Database, **kwargs):
    """
    Function for changing task's executing time
    :key tid: Task id
    """
    pass
# ----- #


FUNCS = {
    'channels.get': channels_get,
    'channels.save': channels_save,
    'sources.get': sources_get,
    'sources.save': sources_save,
    'tasks.get_date': tasks_get_date,
    'tasks.prolong': tasks_prolong
}
