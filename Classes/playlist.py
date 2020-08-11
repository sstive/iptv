class Playlist:

    def __init__(self, **params):
        # Required
        self.owner = params['owner']
        self.channels = params['channels']

        # Optional
        if 'id' in params.keys():
            self.pid = params['id']
        else:
            self.pid = None

        if 'quality' in params.keys():
            self.quality = params['quality']
        else:
            self.quality = 0

        if 'creating_date' in params.keys():
            self.creating_date = params['creating_date']
        else:
            self.creating_date = None

        if 'changing_date' in params.keys():
            self.changing_date = params['changing_date']
        else:
            self.changing_date = None

        if 'del_channels' in params.keys():
            self.del_channels = params['del_channels']
        else:
            self.del_channels = False
