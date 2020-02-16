import m3u8
import os
from updater.data import themes_names
from updater.database import Database
from updater.playlist import Playlist

print('Updating playlists...', end=' ')

db = Database(True)

# Getting forms
forms = db.get_playlists_forms()

# Getting channels id
channels = db.get_channels()

# Adding default form
forms.append(Playlist(0, 'default', 1, []))

for form in forms:
    playlist = m3u8.loads('#EXTM3U')
    # Adding channels to first positions
    for ch in form.channels:
        url = f"{os.environ.get('URL')}/pictures?pic=not_found"
        theme = 0
        if ch in channels.keys():
            u = channels[ch].get_url(form.quality)
            if u != 404:
                url = u
            theme = themes_names[channels[ch].theme]
            channels[ch] = ''
        seg = m3u8.Segment(title=ch, duration=-1, uri=url)
        seg.add_part(f'#EXTGRP: {theme}')
        playlist.add_segment(seg)

    for k in channels.keys():
        ch = channels[k]

        if not ch:
            continue

        if ch.name in form.channels:
            continue

        url = channels[ch.name].get_url(form.quality)
        if url == 404:
            continue

        seg = m3u8.Segment(title=ch.name, duration=-1, uri=url)
        seg.add_part(f'#EXTGRP: {themes_names[ch.theme]}')
        playlist.add_segment(seg)

    db.save_playlist(form.id, playlist.dumps())

print('Done!')
