from Classes import Channel
from DBHelper import Database
from os import environ as env


# Function to generating m3u8 string of channel
def channel_to_m3u8(channel, themes, quality, remove):
    resp = ""
    url = channel.get_url(quality)

    # Adding empty url (or not)
    if url is None:
        if remove:
            return ""
        else:
            url = env['URL'] + '/files/images/not_found.jpg'

    # Adding theme
    if channel.theme is not None:
        resp += f"#EXTGRP:{themes[channel.theme]}\n"

    # Adding channel
    resp += f"#EXTINF:-1,{channel.name}\n"
    resp += url + '\n'

    return resp


def generate_playlist(pl_id: int, db: Database):
    # Adding header
    resp = "#EXTM3U\n"

    # Getting objects from database
    themes = db.run('themes.get')

    # Getting channels from database
    channels = []
    # Filling gaps with None type
    for db_channel in db.select('channels', '*', "ORDER BY id"):
        while len(channels) <= db_channel[0]:
            channels.append(None)
        channels[db_channel[0]] = Channel(*db_channel)

    if pl_id == 0:
        # Default playlist
        request = [('1,2,3', 0, True)]
    else:
        # Getting playlist from database
        request = db.select('playlists', ['channels', 'quality', 'del_channels'], f"WHERE id = {pl_id}")

    # Playlist could be empty
    if len(request) < 1:
        return None

    # Getting info about playlist
    channels_id, quality, remove = request[0]
    # Converting channels ids from str to list
    channels_id = list(map(int, channels_id.split(',')))

    # Adding main channels
    for ch_id in channels_id:
        # Getting channel from list
        channel = channels[ch_id]
        # Removing channel from list to avoid duplicating
        channels[ch_id] = None

        if channel is not None:
            resp += channel_to_m3u8(channel, themes, quality, False)

    # Adding other channels
    for channel in channels:
        if channel is not None:
            resp += channel_to_m3u8(channel, themes, quality, remove)

    return resp
