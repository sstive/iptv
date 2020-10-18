import time
import threading
from os import environ as env
from datetime import datetime
from Utils import parser, utils
from Classes import Channel, task


BANNED_BEGIN_NAME = ['=', '-', '!', '_']
MAX_THREADS = 256
if 'MAX_THREADS' in env.keys():
    MAX_THREADS = env['MAX_THREADS']


class Updater(task.Task):
    # Task id
    tid = 1

    # Threads #
    threads = []
    threads_started = False

    def thread_cleaner(self):
        while len(self.threads) > 0 or self.threads_started:
            if not self.threads_started:
                print(f'\r\t- Checking urls... \t{MAX_THREADS - len(self.threads)}/{MAX_THREADS}', end='')
            i = 0
            time.sleep(1)
            while i < len(self.threads):
                if not self.threads[i].is_alive():
                    del self.threads[i]
                else:
                    i += 1
    # ------- #

    # TODO: separate on functions
    def _execute(self):
        # Step 1: Get sources and channels from database
        # Step 2: Get urls from sources and add them to channels
        # Step 3: Check channel's urls
        # Step 4: Save channels and sources to database

        print("Executing source updater...")

        # Getting objects from database #
        print("\t- Getting objects from database...", end=' ')
        themes = self.DB.run('themes.get')
        channels = self.DB.run('channels.get')
        sources = self.DB.run('sources.get')
        print("Done!")

        # Adding default themes
        print("\t- Checking themes...", end=' ')
        if len(themes) < 13 or themes[:12].count(None) > 1:
            self.DB.run('themes.add_default')
        print("Done!")

        # Getting sources (parsing m3u8) #
        print("\t- Getting sources...", end=' ')
        done = 0
        for source in sources:
            # Progress
            done += 1
            print(f"\r\t- Getting sources... \t{done}/{len(sources)}", end='')

            playlist = parser.load(source['url'])

            if playlist is None:
                if source['last_online'] is not None:
                    source['last_online'] = source['last_online'].strftime("%Y-%m-%d")
                continue

            # Updating sources
            source['count'] = len(playlist)
            source['last_online'] = datetime.now().date().strftime("%Y-%m-%d")

            # Adding urls to channels #
            for segment in playlist:
                # TODO: Refactor
                # Normalising name
                title, quality = Channel.fix_name(segment['title'])

                # Removing useless channels
                if title[0] in BANNED_BEGIN_NAME:
                    continue

                # Searching channel in array
                found = False
                for channel in channels:
                    if channel.name == title:
                        found = True
                        channel.add_url(segment['uri'], quality)
                        break

                # Creating new if not found
                if not found:
                    # Adding new theme
                    theme_id = None
                    theme = utils.fix_theme(segment['group_title'])
                    if theme is not None:
                        if theme in themes:
                            theme_id = themes.index(theme)
                        else:
                            theme_id = self.DB.run('themes.add', theme=theme)
                            while len(themes) < theme_id + 1:
                                themes.append(None)
                            themes[theme_id] = theme
                    # Creating new channel
                    channels.append(Channel(name=title, theme=theme_id, url=(segment['uri'], quality), source_id=source['id']))

        # Disconnecting from database
        self.DB.end()

        print("\r\t- Getting sources... Done!")

        # Checking channels urls #
        # Starting threads
        self.threads_started = True
        thread_cleaner = threading.Thread(target=self.thread_cleaner)
        thread_cleaner.start()

        done = 0
        for channel in channels:
            # Printing progress
            done += 1
            print(f'\r\t- Checking urls... \t{done}/{len(channels)} \t{len(self.threads)}', end='')
            # Waiting for vacant space
            while threading.active_count() >= MAX_THREADS:
                time.sleep(1)
            # Adding thread
            checker = threading.Thread(target=channel.check)
            self.threads.append(checker)
            self.threads[-1].start()

        # Waiting for ending
        self.threads_started = False
        thread_cleaner.join()
        print(f'\r\t- Checking urls... Done!')

        # Starting db connection
        self.DB.begin()

        # Saving sources to database (last online, etc) #
        print("\t- Saving sources...", end=" ")
        self.DB.run('sources.save', sources=sources)
        print("Done!")

        # Saving channels #
        self.DB.run('channels.save', channels=channels)
        print("")

        # Closing db connection
        self.DB.end()

        print("Done!\n")
