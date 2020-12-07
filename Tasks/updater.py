import time
import threading
from datetime import datetime
from Utils import parser, utils
from Classes import Channel, task


BANNED_BEGIN_NAME = ['=', '-', '!', '_']


class Updater(task.Task):
    # Task id #
    tid = 1

    # Threads #
    threads = []

    # Database #
    themes = []
    sources = []
    channels = []

    def clean_threads(self, use_timeout=False):
        i = 0
        while i < len(self.threads):
            if not self.threads[i].is_alive():
                self.threads[i].join()
                del self.threads[i]
            elif use_timeout:
                self.threads[i].join(3)
                del self.threads[i]
            else:
                i += 1
    # ------- #

    def _execute(self):
        print("Executing source updater...")

        # Step 1: Get sources and channels from database
        self.get_database()

        # Step 2: Get urls from sources and add them to channels
        self.get_sources()

        # Step 3: Check channel's urls
        self.check_urls()

        # Step 4: Save channels and sources to database
        self.save_databases()

        print("Done!\n")

    # Getting objects from database #
    def get_database(self):
        print("\t- Getting objects from database...", end=' ')
        self.themes = self.DB.run('themes.get')
        self.channels = self.DB.run('channels.get')
        self.sources = self.DB.run('sources.get')
        print("Done!")

        # Adding default themes
        print("\t- Checking themes...", end=' ')
        if len(self.themes) < 13 or self.themes[:12].count(None) > 1:
            self.DB.run('themes.add_default')

        # Disconnecting from database
        self.DB.end()

        print("Done!")

    # Getting sources (parsing m3u8) #
    def get_sources(self):
        print("\t- Getting sources...", end=' ')
        done = 0
        for source in self.sources:
            # Progress
            done += 1
            print(f"\r\t- Getting sources... \t{done}/{len(self.sources)}", end='')

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
                for channel in self.channels:
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
                        if theme in self.themes:
                            theme_id = self.themes.index(theme)
                        else:
                            theme_id = self.DB.run('themes.add', theme=theme)
                            while len(self.themes) < theme_id + 1:
                                self.themes.append(None)
                            self.themes[theme_id] = theme
                    # Creating new channel
                    self.channels.append(
                        Channel(name=title, theme=theme_id, url=(segment['uri'], quality), source_id=source['id'])
                    )

        # Disconnecting from database
        self.DB.end()

        print("\r\t- Getting sources... Done!")

    # Checking channels urls #
    def check_urls(self):
        print('\t- Checking urls...')

        # Checking delay
        delay = self.MAX_THREADS // 100

        done = 0
        for channel in self.channels:
            # Printing progress
            done += 1
            print(f'\r\t\t- Adding treads ({len(self.threads)} is active): {done}/{len(self.channels)}', end='')

            # Waiting for vacant space
            while threading.active_count() >= self.MAX_THREADS:
                time.sleep(delay)
                self.clean_threads()

            # Adding thread
            checker = threading.Thread(target=channel.check, daemon=True)
            self.threads.append(checker)
            del checker
            self.threads[-1].start()

        # Waiting for ending
        print()
        while len(self.threads) > 0:
            time.sleep(delay)
            self.clean_threads(len(self.threads) <= 10)
            print(f'\r\t\t- Checking {self.MAX_THREADS - len(self.threads)}/{self.MAX_THREADS}', end='')

        print(f'\n\t- Done!')

    def save_databases(self):
        # Starting db connection
        self.DB.begin()

        # Saving sources to database (last online, etc) #
        print("\t- Saving sources...", end=" ")
        self.DB.run('sources.save', sources=self.sources)
        print("Done!")

        # Saving channels #
        self.DB.run('channels.save', channels=self.channels)
        print("")

        # Closing db connection
        self.DB.end()
