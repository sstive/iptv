import m3u8
import os
from updater.data import Qualities, themes_names
from updater.channel import Channel
from updater.database import Database
from updater.utils import Utils
from updater.playlist import Playlist
# TODO: replace print with logging

# Connecting to database
db = Database()

# Getting sources
sources = db.get_sources()

# Getting channels
channels = db.get_channels()

del db

print('Updating channels...')
for src in sources:
    # Opening playlist
    try:
        form = m3u8.loads(Utils.get(src.url, 3))
    except Exception as e:
        print(f'\t{e}')
        src.add_unavailable_days()
        continue

    src.reset_unavailable_days()
    src.channels = len(form.segments)

    # Working with channels
    for c in form.segments:
        quality = 0

        title = c.title.strip()
        words = title.split()

        # Defining quality
        for q in Qualities:
            for Qlable in q:
                for word in words:
                    if word.lower() == Qlable:
                        quality = Qualities.index(q)
                        if words.index(word) > 0 and len(words) > 1:
                            words.remove(word)
                            title = ' '.join(words).strip()
                        break

        if title in channels.keys():
            # If channel already in array
            channel = channels[title]
        else:
            # Create new channel
            channel = Channel(title)

        # Adding url to channel
        if not channel.add_url(c.uri, quality, True):
            print(f'\r ({form.segments.index(c)}/{src.channels})')
            continue

        src.add_available()

        # Saving to array
        channels[title] = channel
    db = Database (True)
    # Saving to database
    db.add_channels(channels)
    del db

db = Database (True)
db.update_sources(sources)

print('Updating playlists...', end=' ')
# Getting forms
forms = db.get_playlists_forms()

# Getting channels id
channels.clear()
channels = db.get_channels()

# Adding default form
forms.append(Playlist(0, 'default', 1, []))

for form in forms:
    playlist = m3u8.loads('#EXTM3U')
    for ch in form.channels:
        url = f"{os.environ.get('URL')}/pictures?pic=not_found"
        theme = 0
        if ch in channels.keys():
            url = f"{os.environ.get('URL')}/channel?id={channels[ch].id}&q={form.quality}"
            theme = themes_names[channels[ch].theme]
        seg = m3u8.Segment(title=ch, duration=-1, uri=url)
        seg.add_part(f'#EXTGRP: {theme}')
        playlist.add_segment(seg)

    for k in channels.keys():
        ch = channels[k]
        if ch not in form.channels:
            seg = m3u8.Segment(title=ch.name, duration=-1, uri=f"{os.environ.get('URL')}/channel?id={ch.id}&q={form.quality}")
            seg.add_part(f'#EXTGRP: {themes_names[ch.theme]}')
            playlist.add_segment(seg)

    db.save_playlist(form.id, playlist.dumps())

print('Done!')
