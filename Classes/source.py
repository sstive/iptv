class Source:

    def __init__(self, **params):
        self.url = params['url']

        if 'id' in params.keys():
            self.sid = params['id']
        else:
            self.sid = None

        if 'last_online' in params.keys():
            self.last_online = params['last_online']
        else:
            self.last_online = None

        if 'channels' in params.keys():
            self.channels = params['channels']
        else:
            self.ch_available = []

        if 'count' in params.keys():
            self.count = params['count']
        else:
            self.count = 0

        if 'available' in params.keys():
            self.available = params['available']
        else:
            self.available = 0
