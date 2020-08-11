class Channel:

    def __init__(self, **params):
        self.name = params['name']

        # Id
        if 'id' in params.keys():
            self.cid = params['id']
        else:
            self.cid = None

        # Theme
        if 'group' in params.keys():
            self.group = params['group']
        else:
            self.group = None
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

        # Actions for new channels from playlist
        if not ('from_db' in params.keys() and params['from_db']):
            # Editing name
            self.__check_name__()

    def __find_theme__(self):
        # TODO: find theme of channel
        pass

    # Removing HD, FHD and other words from channels name
    def __check_name__(self):
        # TODO: remove HD FHD and other from channels name
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
