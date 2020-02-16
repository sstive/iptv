import m3u8
from updater.data import Qualities
from updater.channel import Channel
from updater.database import Database
from updater.utils import Utils

db = Database(True)
channels = db.get_channels()

# Getting sources
sources = db.get_sources()
del db

print('Updating channels...')
for src in sources:
    # Opening playlist
    try:
        source = m3u8.loads(Utils.get(src.url, 3))
    except Exception as e:
        print(f'\t{e}')
        src.add_unavailable_days()
        continue

    src.reset_unavailable_days()
    src.channels = len(source.segments)

    # Working with channels
    for c in source.segments:
        quality = 0

        title = c.title.strip().replace('"', '*')
        words = title.split()

        if title[0] == '-':
            continue

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
            print(f'\t({source.segments.index(c)}/{src.channels})')
            continue

        src.add_available()

        # Saving to array
        channels[title] = channel

db = Database(True)
db.update_sources(sources)

db.add_channels(channels)

del db
