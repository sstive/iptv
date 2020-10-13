from Classes import Channel
from Utils.db_functions import FUNCS
from DBHelper import Database
from os import environ as env


def channel_to_m3u8(channel, themes, quality, remove):
    resp = ""
    url = channel.get_url(quality)
    if url is None:
        if remove:
            return ""
        else:
            url = env['URL'] + '/picture/not_found'

    if channel.theme is not None:
        resp += f"#EXTGRP:{themes[channel.theme]}\n"

    resp += f"#EXTINF:-1,{channel.name}\n"
    resp += url + '\n'

    return resp


def generate_playlist(pl_id: int):
    db = Database('../Config/Database.json', functions=FUNCS)

    resp = "#EXTM3U\n"
    themes = db.run('themes.get')
    channels = db.run('channels.get')

    if pl_id == 0:
        request = [('1,2,3', 0, True)]
    else:
        request = db.select('playlists', ['channels', 'quality', 'del_channels'], f"WHERE id = {pl_id}")

    if len(request) < 1:
        return None

    channels_id, quality, remove = request[0]
    channels_id = list(map(int, channels_id.split(',')))

    # TODO: remove repeating code

    # Adding main channels
    for ch_id in channels_id:
        # Getting channel from list
        channel = channels[ch_id]
        # Removing channel from list to avoid duplicating
        channels[ch_id] = None

        resp += channel_to_m3u8(channel, themes, quality, remove)

    # Adding other channels
    for channel in channels:
        if channel is not None:
            resp += channel_to_m3u8(channel, themes, quality, remove)

    return resp
