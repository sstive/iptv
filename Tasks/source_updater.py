from datetime import datetime
from threading import Thread
from urllib.error import HTTPError, URLError

import m3u8

from Classes import Task, Channel


class SourceUpdater(Task):

    @staticmethod
    def fix_name(name):
        quality = 0
        # TODO: Prepare name (Remove HD, ", etc)
        return name, quality

    def execute(self):
        print("Executing source updater...")

        # Getting objects from database #
        print("\t- Getting objects from database...", end=' ')
        channels = self.DB.run('channels.get')
        sources = self.DB.run('sources.get')
        print("Done!")

        # Disconnect from database
        self.DB.end()

        # Getting sources (parsing m3u8) #
        print("\t- Getting sources...", end=' ')
        for source in sources:
            # Trying to parse m3u8
            try:
                playlist = m3u8.load(source['url'])
            except HTTPError or URLError:
                continue
            except ValueError:
                # TODO: fix groups
                continue

            # Updating sources
            sources['count'] = len(playlist.data['segments'])
            sources['last_online'] = datetime.now()

            # Adding urls to channels #
            for segment in playlist.data['segments']:
                # Normalising name
                title, quality = self.fix_name(segment['title'])

                # Searching channel in array
                found = False
                for channel in channels:
                    if channel.name == title:
                        channel.add_url(segment['uri'], quality)
                        found = True
                        break

                # Creating new if not found
                if not found:
                    channels.append(Channel(name=title, url=(segment['uri'], quality)))
        print("Done")

        # Checking channels urls #
        print("\t- Checking urls...", end=" ")

        # Starting threads
        threads = []
        for channel in channels:
            checker = Thread(target=channel.check)
            threads.append(checker)
            threads[-1].start()

        # Waiting for ending
        while len(threads) > 0:
            i = 0
            while i < len(threads):
                if not threads[i].is_alive():
                    del threads[i]
                else:
                    i += 1
        print("Done")

        # Starting db connection
        self.DB.begin()

        # Saving sources to database (last online, etc) #
        print("\t- Saving sources...", end=" ")
        self.DB.run('sources.save', sources=sources)
        print("Done!")

        # Saving channels #
        print("\t- Saving channels...", end=" ")
        self.DB.run('channels.save', channels=channels)
        print("Done!")

        print("Done!")
