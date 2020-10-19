from Utils.utils import replace_symbols, check_url
from Config.variables import QUALITIES, THEMES


class Channel:

    def __init__(self, *db_params, **params):
        """
        Class for channel, contain info about channel and functions for it.
        :param db_params: Array with params, loaded from database
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

        # Converting db_params
        if len(db_params) >= 6:
            params['id'] = db_params[0]
            params['name'] = db_params[1]
            params['theme'] = db_params[2]
            params['urls'] = db_params[3]
            params['online'] = db_params[4]
            params['source_id'] = db_params[5]

        # Cutting name
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
        if 'theme' in params.keys() and params['theme'] is not None:
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
        self.theme = THEMES['default']
        for t_name, channels in THEMES['themes'].items():
            if self.name in channels:
                self.theme = list(THEMES['themes'].keys()).index(t_name)
                break

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

    # Return online as number
    def __get_online__(self):
        online = 0
        for q in self.online:
            if q:
                online += 1
            online *= 2
        online //= 2
        return online

    # Public #
    def add_url(self, url, quality=0):
        # If quality is string
        if type(quality) is str:
            qs = ['sd', 'hd', 'fhd', 'qhd']
            self.urls[qs.index(quality)].append(url)
        # If quality is number
        else:
            self.urls[quality].append(url)

    # Convert urls to string for database
    def get_urls(self):
        urls = ""
        for q in self.urls:
            urls += ','.join(q)
            urls += ';'
        return urls

    def get_url(self, quality):
        url = None
        for i in range(quality, -1, -1):
            if self.online[i]:
                url = self.urls[i][0]
                break
        return url

    # Checking urls
    def check(self):
        for i in range(0, len(self.urls)):
            for url in self.urls[i]:
                if not check_url(url):
                    self.urls[i].remove(url)

        self.__set_online__()
        return True

    # Convert channel to dict
    def get_dict(self):
        d = {
            'id': self.cid,
            'name': self.name,
            'theme': self.theme,
            'urls': self.get_urls(),
            'online': self.__get_online__(),
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
        name = replace_symbols(name, ('_', ' '), ('|', ' '), '(ForkPlayer)')

        # Finding quality
        words = name.strip().split()
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
                    found = True

                    # Removing composing quality text
                    if fixed_words.index(alias[1]) == len(fixed_words) - 1:
                        words = words[:-2]
                    break
                # Checking simple single word alias
                elif type(alias) is str and alias in fixed_words:
                    quality = QUALITIES['names'].index(q)
                    found = True

                    # Removing single quality text
                    if fixed_words.index(alias) == len(fixed_words) - 1:
                        words = words[:-1]
                    break
            if found:
                break

        # Formatting name
        name = ' '.join(words)
        if len(name) > 5:
            name.title()
        else:
            name.upper()

        return name, quality
    # ------ #
