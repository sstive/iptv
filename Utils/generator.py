from Classes import Channel
from Utils.db_functions import FUNCS
from DBHelper import Database
from os import environ as env


def generate_playlist(pl_id: int):
    db = Database('Config/Database.json', functions=FUNCS)

    OUT = ['#EXTM3U']
    themes = db.run('themes.get')

    request = db.select('playlists', ['channels', 'quality'], f"WHERE id = {pl_id}")
    if len(request) < 1:
        return None

    channels_id, quality = request[0]
    channels_id = list(map(int, channels_id.split(',')))

    for ch_id in channels_id:
        channel = Channel(*db.select('channels', '*', f"WHERE ID = {ch_id}")[0])

        url = channel.get_url(quality)
        if url is None:
            url = env['URL'] + '/picture/not_found'

        if channel.theme is not None:
            OUT.append('#EXTGRP:' + themes[channel.theme])
        OUT.append('#EXTINF:-1,' + channel.name)
        OUT.append(url)

    return OUT
