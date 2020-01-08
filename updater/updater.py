import m3u8
from data import Qualities, themes_names
from channel import Channel
from database import Database
from utils import Utils
from playlist import Playlist

# Connecting to database
db = Database()

sources = []#db.get_sources()

channels = db.get_channels()

print('Updating channels...')
for src in sources:
    # Opening playlists
    try:
        pl = m3u8.loads(Utils.get(src.url, 3))
        print(pl)
    except Exception as e:
        print(f'\t{e}')
        src.src_available = False
        continue

    src.channels = len(pl.segments)
    src.available = 0

    # Working with channels
    for c in pl.segments:
        # Checking connection to url
        if not Utils.check_connection(c.uri):
            continue

        src.add_available()

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
        channel.add_url(c.uri, quality)

        # Saving to array
        channels[title] = channel

    # Saving to database
    db.add_channels(channels)

db.update_sources(sources)

print('Updating playlists...', end=' ')

channels = db.get_channels()
playlists = db.get_playlists()

playlists.append(Playlist('default', 1, []))

for pl in playlists:
    playlist = m3u8.loads('#EXTM3U')
    for ch in pl.channels:
        url = 'http://iptv.pythonanywhere.com/pictures?pic=not_found'
        theme = 0
        if ch in channels.keys():
            url = f'http://iptv.pythonanywhere.com/channel?id={channels[ch].id}&q={pl.quality}'
            theme = themes_names[channels[ch].theme]
        seg = m3u8.Segment(title=ch, duration=-1, uri=url)
        seg.add_part(f'#EXTGRP: {theme}')
        playlist.add_segment(seg)

    for k in channels.keys():
        ch = channels[k]
        if ch not in pl.channels:
            seg = m3u8.Segment(title=ch.name, duration=-1, uri=f'http://iptv.pythonanywhere.com/channel?id={ch.id}&q={pl.quality}')
            seg.add_part(f'#EXTGRP: {themes_names[ch.theme]}')
            playlist.add_segment(seg)

    playlist.dump(f'playlists/{pl.name}.m3u8')

print('Done!')
