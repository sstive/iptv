class Channel:

    def __init__(self, **params):
        """
        Class for channel, contain info about channel and functions for it.
        :param params: Params of channel

        :key name: Title of channel, should be str
        :key id: Id of channel in database, should be int
        :key theme: Id of theme, should be int
        :key online: Is channel online, should be boolean
        :key urls: Array with urls [quality][urls], should be list
        :key url: Param for adding default url (url, quality), should be tuple
        """
        self.name = params['name']

        # Id
        if 'id' in params.keys():
            self.cid = params['id']
        else:
            self.cid = None

        # Theme
        if 'theme' in params.keys():
            self.theme = params['group']
        else:
            self.theme = None
            self.__find_theme__()

        # Online
        # TODO: make last online on every url
        if 'online' in params.keys():
            self.online = params['online']
        else:
            self.online = True

        # Urls
        if 'urls' in params.keys():
            self.urls = self.__urls_to_list__(params['urls'])
        else:
            self.urls = [
                [],     # SD
                [],     # HD
                [],     # FHD
                []      # QHD
            ]

        # Adding single url (tuple)
        if 'url' in params.keys():
            self.urls[params['url'][1]] = params['url'][0]

    def __find_theme__(self):
        # TODO: find theme of channel
        pass

    @staticmethod
    def __urls_to_list__(urls):
        if type(urls) is list:
            return urls
        elif type(urls) is dict:
            new_urls = [[], [], [], []]
            if 'sd' in urls.keys():
                new_urls[0] = urls['sd']
            if 'hd' in urls.keys():
                new_urls[1] = urls['hd']
            if 'fhd' in urls.keys():
                new_urls[2] = urls['fhd']
            if 'qhd' in urls.keys():
                new_urls[3] = urls['qhd']
            return new_urls

    # Public #

    def add_url(self, url, quality=0):
        # If quality is string
        if type(quality) is str:
            qs = ['sd', 'hd', 'fhd', 'qhd']
            self.urls[qs.index(quality)].append(url)
        # If quality is number
        else:
            self.urls[quality].append(url)

    def check(self):
        # TODO: check connection to channel
        pass
