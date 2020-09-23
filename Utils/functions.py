from DBHelper import Database


# Params:
def get_channels(db: Database, **kwargs):
    print(db.select('*', 'channels'))


FUNCS = {
    'channels.get': get_channels,
    'channels.save': None,
    'sources.get': None,
    'sources.save': None,
    'tasks.get_date': None,
    'tasks.prolong': None
}
