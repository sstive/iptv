import m3u8
from classes.data import Qualities
from classes.channel import Channel
from classes.database import Database
from classes.utils import Utils

db = Database()
channels = db.get_channels()

# Getting sources
sources = db.get_sources()
del db

print('Updating channels...')
for src in sources:
    # Opening playlist
    print(f'\tGetting source {src.url} ...', end=' ')
    try:
        source_pl = m3u8.loads(Utils.get(src.url, 3))
    except Exception as e:
        print(f'\t{e}')
        src.add_unavailable_days()
        continue

    print('Done!')

    src.reset_unavailable_days()
    src.channels = len(source_pl.segments)

    # Working with channels
    for channel_pl in source_pl.segments:
        quality = 0

        title = channel_pl.title.strip().replace('"', '*')
        words = title.split()

        if title[0] in ['=', '-', '#', ':', '*']:
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

        found = False
        str = Utils.prepare_to_compare(title)
        for key in channels.keys():
            if Utils.prepare_to_compare(key) == str:
                found = True
                title = key
                break

        if found:
            # If channel already in array
            channel = channels[title]
        else:
            # Create new channel
            channel = Channel(title)

        # Adding url to channel
        if not channel.add_url(channel_pl.uri, quality, False):
            print('Can\'t connect!', end=' ')
            continue

        src.add_available()
        print(f'\t({source_pl.segments.index(channel_pl)}/{src.channels})')
        # Saving to array
        channels[title] = channel

db = Database(True)
db.update_sources(sources)

db.add_channels(channels)

del db

print('New urls received!')
