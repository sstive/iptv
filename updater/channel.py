from utils import Utils
from data import themes


class Channel:

    def __init__(self, name, theme=0, id=0):
        self.id = id
        self.name = name
        self.label = Utils.to_eng(name)
        self.theme = theme

        self.urls_sd = []
        self.urls_hd = []
        self.urls_fhd = []
        self.urls_uhd = []

        if self.theme == 0:
            self.__define_theme__()

    def __define_theme__(self):
        for theme in themes:
            if Utils.prepare_to_compare(self.name) in theme:
                self.theme = themes.index(theme) + 1
                return

    def add_str_urls(self, str_urls, quality):
        if str_urls == '':
            return False
        urls = str_urls.split(',')
        for url in urls:

            if quality == 0:
                if url in self.urls_sd:
                    return False
                self.urls_sd.append(url.strip())

            elif quality == 1:
                if url in self.urls_hd:
                    return False
                self.urls_hd.append(url.strip())

            elif quality == 2:
                if url in self.urls_fhd:
                    return False
                self.urls_fhd.append(url.strip())

            else:
                if url in self.urls_uhd:
                    return False
                self.urls_uhd.append(url.strip())

    def get_str_urls(self, quality=0):
        if quality == 0:
            return ','.join(self.urls_sd)
        elif quality == 1:
            return ','.join(self.urls_hd)
        elif quality == 2:
            return ','.join(self.urls_fhd)
        else:
            return ','.join(self.urls_uhd)

    def add_url(self, url, quality=0):
        if quality == 0:
            self.urls_sd.append(url)
        elif quality == 1:
            self.urls_hd.append(url)
        elif quality == 2:
            self.urls_fhd.append(url)
        else:
            self.urls_uhd.append(url)

    def get_id(self):
        if self.id:
            return self.id
        return False

    def get_url(self, quality):
        urls = [self.urls_sd, self.urls_hd, self.urls_fhd, self.urls_uhd]

        for i in range(quality, -1, -1):
            for url in urls[i]:
                return url
        return False
