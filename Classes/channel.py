import urllib.request


# Additional methods #
def replace_symbols(s: str, *chars):
    for char in chars:
        if type(char) is tuple:
            s = s.replace(char[0], char[1])
        elif type(char) is str:
            s = s.replace(char, '')
    return s


# ------------------ #


# Additional variables #
QUALITIES = {
    "default": 'SD',
    'symbols': ['[', ']', '(', ')', '{', '}'],
    "names": ['SD', 'HD', 'FHD', 'QHD', 'UHD'],
    # Reversed because in higher qualities more words
    "aliases": {
        'UHD': [
            "uhd",
            "4k",
            "8k",
            ["ultra", "hd"]
        ],
        'QHD': [
            "qhd",
            "2k",
            "1440p",
            ["quad", "hd"]
        ],
        'FHD': [
            "fhd",
            "1080p",
            ["full", "hd"]
        ],
        'HD': [
            "hd",
            "720p"
        ]
    }
}


# -------------------- #


class Channel:

    def __init__(self, **params):
        """
        Class for channel, contain info about channel and functions for it.
        :param params: Params of channel

        :key name: Title of channel, should be str
        :key id: Id of channel in database, should be int
        :key theme: Id of theme, should be int
        :key group_title: Title of group
        :key online: Is channel online (for every quality), should be list
        :key urls: Array with urls [quality][urls], should be list
        :key url: Param for adding default url (url, quality), should be tuple
        :key source: Id of source
        """
        # TODO: Refactor
        if len(params['name']) < 50:
            self.name = params['name']
        else:
            self.name = params['name'][:50]

        # Id
        if 'id' in params.keys():
            self.cid = params['id']
        else:
            self.cid = None

        # Theme
        if 'theme' in params.keys():
            self.theme = params['theme']
        else:
            self.theme = None
            self.__find_theme__()

        # Online
        if 'online' in params.keys():
            self.online = params['online']
        else:
            self.online = [False, False, False, False, False]
        self.__convert_online__()

        # Source id
        if 'source_id' in params.keys():
            self.source_id = params['source_id']

        # Urls
        if 'urls' in params.keys():
            self.urls = params['urls']
        else:
            self.urls = [
                [],  # SD
                [],  # HD
                [],  # FHD
                [],  # QHD
                []  # UHD
            ]
        self.__convert_urls__()

        # Adding single url (tuple)
        if 'url' in params.keys():
            url, q = params['url']
            self.urls[q].append(url)

    def __find_theme__(self):
        # TODO: find theme of channel
        pass

    # Convert urls from string to dict
    def __convert_urls__(self):
        if type(self.urls) is not str:
            return
        self.urls = self.urls.split(';')
        for i in range(0, len(self.urls)):
            self.urls[i] = self.urls[i].split(',')

    def __set_online__(self):
        for i in range(0, len(self.online)):
            self.online[i] = len(self.urls[i]) > 0

    # Convert online to boolean list
    def __convert_online__(self):
        if type(self.online) is not int:
            return

        # [SD, HD, FHD, QHD, UHD]
        online = self.online
        self.online = []
        while online > 0:
            if online % 2 == 1:
                self.online.append(True)
            else:
                self.online.append(False)
            online //= 2

        # Adding zeroes
        while len(self.online) < 5:
            self.online.append(False)
        self.online.reverse()

    # Public #
    def add_url(self, url, quality=0):
        # If quality is string
        if type(quality) is str:
            qs = ['sd', 'hd', 'fhd', 'qhd']
            self.urls[qs.index(quality)].append(url)
        # If quality is number
        else:
            self.urls[quality].append(url)

    # Return online as number
    def get_online(self):
        online = 0
        for q in self.online:
            if q:
                online += 1
            online *= 2
        online //= 2
        return online

    # Convert urls to string for database
    def get_urls(self):
        return ';'.join(list(map(lambda urls: ','.join(urls), self.urls)))

    # Checking urls
    def check(self):
        for i in range(0, len(self.urls)):
            for url in self.urls[i]:
                try:
                    if urllib.request.urlopen(url, timeout=3).getcode() == 200:
                        continue
                except Exception:
                    pass

                self.urls[i].remove(url)
        self.__set_online__()

    # Convert channel to dict
    def get_dict(self):
        d = {
            'id': self.cid,
            'name': self.name,
            'theme': self.theme,
            'urls': self.get_urls(),
            'online': self.get_online(),
            'source_id': self.source_id
        }

        # Finding empty values
        delete = []
        for k, v in d.items():
            if v is None:
                delete.append(k)

        # Deleting empty values
        for k in delete:
            del d[k]

        return d

    # -------- #

    # Static #
    @staticmethod
    def fix_name(name: str):
        # Replacing symbols
        name = replace_symbols(name, ('_', ' '))

        # Finding quality
        words = name.split()
        fixed_words = replace_symbols(name, *QUALITIES['symbols']).lower().split()
        quality = 0
        found = False

        for q, aliases in QUALITIES['aliases'].items():
            for alias in aliases:
                # Checking composing aliases
                if (
                        type(alias) is list and
                        alias[0] in fixed_words and alias[1] in fixed_words and
                        fixed_words.index(alias[0]) == fixed_words.index(alias[1]) - 1
                ):
                    quality = QUALITIES['names'].index(q)

                    # Removing composing quality text
                    if fixed_words.index(alias[1]) == len(fixed_words) - 1:
                        words = words[:-2]
                        found = True
                    break
                # Checking simple single word alias
                elif type(alias) is str and alias in fixed_words:
                    quality = QUALITIES['names'].index(q)

                    # Removing single quality text
                    if fixed_words.index(alias) == len(fixed_words) - 1:
                        words = words[:-1]
                        found = True
                    break
            if found:
                break

        return ' '.join(words), quality
    # ------ #
