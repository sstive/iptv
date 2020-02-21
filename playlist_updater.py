import m3u8
import os

from classes.channel import Channel
from classes.data import themes_names
from classes.database import Database
from classes.form import Form
from classes.utils import Utils

print('Updating playlists...', end=' ')

db = Database()

# Getting forms
forms = db.get_playlists_forms()

# Getting channels id (dict)
channels = db.get_channels()

del db

playlists = {}
# Adding default form
forms.append(Form(0, 'default', 1, []))

for form in forms:
    playlist = m3u8.loads('#EXTM3U')
    # Adding channels to first positions
    for ch_name in form.channels:
        url = f"{os.environ.get('URL')}/pictures?pic=not_found"
        theme = 0

        found = False
        str = Utils.prepare_to_compare(ch_name)
        for key in channels.keys():
            if Utils.prepare_to_compare(key) == str:
                found = True
                ch_name = key
                break

        if found:
            u = channels[ch_name].get_url(form.quality)
            if u != 404:
                url = u
            theme = channels[ch_name].theme
            channels[ch_name] = ''
        seg = m3u8.Segment(title=ch_name, duration=-1, uri=url)
        seg.add_part(f'#EXTGRP: {themes_names[theme]}')
        playlist.add_segment(seg)

    # Adding other channels
    for ch in channels.values():
        if not isinstance(ch, Channel):
            continue

        if Utils.prepare_to_compare(ch.get_name()) in list(map(lambda x: Utils.prepare_to_compare(x), form.channels)):
            continue

        url = ch.get_url(form.quality)
        if url == 404:
            continue

        form.channels.append(ch.name)

        seg = m3u8.Segment(title=ch.name, duration=-1, uri=url)
        seg.add_part(f'#EXTGRP: {themes_names[ch.theme]}')
        playlist.add_segment(seg)

    playlists[form.id] = playlist.dumps()

db = Database(True)

forms.remove(forms[-1])
db.save_forms(forms)

for id in playlists.keys():
    if id == 0:
        continue
    db.save_playlist(id, playlists[id])

print('Done!')
