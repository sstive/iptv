from data import protocols


class Source:

    def __init__(self, id, protocol, host, channels=0):
        self.id = id
        self.protocol = protocol
        self.host = host
        self.url = protocols[protocol] + '://' + host
        self.channels = channels
        self.ch_available = 0
        self.src_available = True

    def add_available(self):
        self.ch_available += 1
