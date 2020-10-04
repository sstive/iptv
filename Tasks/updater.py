import threading
from threading import Thread
import time
from datetime import datetime
from urllib.error import HTTPError, URLError

import m3u8

from Utils.task import Task
from Classes import Channel


class Updater(Task):

    # Threads #
    threads = []
    threads_started = False

    def thread_cleaner(self):
        while len(self.threads) > 0 or self.threads_started:
            i = 0
            if len(self.threads) > 0:
                print(self.threads[0].name + '\t\t' + str(len(self.threads)) + '\t' + str(threading.active_count()))
            time.sleep(1)
            while i < len(self.threads):
                if not self.threads[i].is_alive():
                    del self.threads[i]
                else:
                    i += 1
        print('sdaadad')
    # ------- #

    @staticmethod
    def fix_name(name):
        # TODO: Prepare name (Remove HD, ", etc)
        return name, 0

    def execute(self):
        print("Executing source updater...")

        # Getting objects from database #
        print("\t- Getting objects from database...", end=' ')
        channels = self.DB.run('channels.get')
        sources = self.DB.run('sources.get')
        print("Done!")

        # Disconnect from database
        self.DB.end()

        # Adding default source
        if len(sources) == 0:
            sources.append({'url': 'https://iptvmaster.ru/russia.m3u', 'last_online': '2020-09-26', 'count': 0})

        # Getting sources (parsing m3u8) #
        print("\t- Getting sources...", end=' ')
        for source in sources:
            # Trying to parse m3u8
            try:
                playlist = m3u8.load(source['url'])
            except ValueError:
                # TODO: fix groups in some playlists ('group-title=')
                continue
            except HTTPError:
                continue
            except URLError:
                continue

            # Updating sources
            source['count'] = len(playlist.data['segments'])
            source['last_online'] = datetime.now().date().strftime("%Y-%m-%d")

            # Adding urls to channels #
            for segment in playlist.data['segments']:
                # Normalising name
                # TODO: Refactor
                title, quality = self.fix_name(segment['title'])

                # Searching channel in array
                found = False
                for channel in channels:
                    if channel.compare(title):
                        found = True
                        channel.add_url(segment['uri'], quality)
                        break

                # Creating new if not found
                if not found:
                    channels.append(Channel(name=title, url=(segment['uri'], quality)))
        print("Done!")

        # Checking channels urls #
        print("\t- Checking urls...", end=" ")

        # Starting threads
        self.threads_started = True
        thread_cleaner = Thread(target=self.thread_cleaner)
        thread_cleaner.start()

        names = {}

        for channel in channels:
            # Waiting for vacant space
            while threading.active_count() >= 700:
                time.sleep(1)
            checker = Thread(target=channel.check)
            self.threads.append(checker)
            self.threads[-1].start()
            names[checker.name] = channel.name

        print(str(names))
        f = open('threads.txt', 'w')
        f.write(str(names))
        f.close()

        # Waiting for ending
        print(threading.active_count())
        self.threads_started = False
        thread_cleaner.join()
        print(f"Done!")

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

        # Closing db connection
        self.DB.end()

        print("Done!")
