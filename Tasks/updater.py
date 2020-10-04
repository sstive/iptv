import time
import threading
from datetime import datetime
from Utils import task, parser
from Classes import Channel


class Updater(task.Task):

    # Threads #
    threads = []
    threads_started = False

    def thread_cleaner(self):
        while len(self.threads) > 0 or self.threads_started:
            i = 0
            time.sleep(1)
            while i < len(self.threads):
                if not self.threads[i].is_alive():
                    del self.threads[i]
                else:
                    i += 1
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
            sources.append({'url': 'https://iptvmaster.ru/russia.m3u', 'last_online': '2020-01-01', 'count': 0})

        # Getting sources (parsing m3u8) #
        print("\t- Getting sources...", end=' ')
        done = 0
        for source in sources:
            # Progress
            print(f"\r\t- Getting sources... \t{done}/{len(sources)}")

            playlist = parser.load(source['url'])

            if playlist is None:
                source['last_online'] = source['last_online'].strftime("%Y-%m-%d")
                continue

            # Updating sources
            source['count'] = len(playlist)
            source['last_online'] = datetime.now().date().strftime("%Y-%m-%d")

            # Adding urls to channels #
            for segment in playlist:
                # TODO: Refactor
                # Normalising name
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
                    channels.append(Channel(name=title, url=(segment['uri'], quality), source_id=source['id']))
        print("Done!")

        # Checking channels urls #
        print("\t- Checking urls...", end=" ")

        # Starting threads
        self.threads_started = True
        thread_cleaner = threading.Thread(target=self.thread_cleaner)
        thread_cleaner.start()

        done = 0
        for channel in channels:
            # Printing progress
            print(f'\r\t- Checking urls... \t{done}/{len(channels)} \t{len(self.threads)}', end='')
            # Waiting for vacant space
            while threading.active_count() >= 700:
                time.sleep(1)
            # Adding thread
            checker = threading.Thread(target=channel.check)
            self.threads.append(checker)
            self.threads[-1].start()
            done += 1

        # Waiting for ending
        self.threads_started = False
        thread_cleaner.join()
        print(f"\r\t- Checking urls... Done!")

        # Starting db connection
        self.DB.begin()

        # Saving sources to database (last online, etc) #
        print("\t- Saving sources...", end=" ")
        self.DB.run('sources.save', sources=sources)
        print("Done!")

        # Saving channels #
        print("\t- Saving channels...", end=" ")
        self.DB.run('channels.save', channels=channels)
        print("\r\t- Saving channels...Done!")

        # Closing db connection
        self.DB.end()

        print("Done!")
