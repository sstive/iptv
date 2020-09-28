import requests
from Classes import Channel


def load(url: str):
    req = requests.get(url)

    if req.status_code != 200:
        return None

    playlist = req.text.split('\n')

    channels = []
    channel = None
    for line in playlist:
        if line[0] == '#':
            parts = line.split(':', 1)
            # TODO: add theme
            if parts[0] == '#EXTGRP':
                pass
            elif parts[0] == '#EXTINF':

                channel = Channel()
        else:
            pass
