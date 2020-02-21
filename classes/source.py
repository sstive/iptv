from classes.data import protocols


class Source:

    def __init__(self, **params):
        if 'id' in params.keys():
            self.id = params['id']
        else:
            self.id = None

        if 'protocol' in params.keys():
            self.protocol = params['protocol']
        else:
            self.protocol = None

        if 'host' in params.keys():
            self.host = params['host']
        else:
            self.host = None

        if 'url' in params.keys():
            self.url = params['url']

            s = self.url.split('://')

            self.protocol = protocols.index(s[0])
            self.host = s[1]
        elif self.protocol and self.host:
            self.url = protocols[self.protocol] + '://' + self.host
        else:
            self.url = None

        if 'unavailable' in params.keys():
            self.unavailable = params['unavailable']
        else:
            self.unavailable = 0

        self.ch_available = 0
        self.channels = 0

    def add_available(self):
        self.ch_available += 1

    def add_unavailable_days(self):
        self.unavailable += 1

    def reset_unavailable_days(self):
        self.unavailable = 0
