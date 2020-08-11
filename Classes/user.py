class User:

    def __init__(self, **params):
        self.name = params['name']
        self.password = params['password']

        # Id
        if 'id' in params.keys():
            self.uid = params['id']
        else:
            self.uid = None

        # E-mail
        if 'email' in params.keys():
            self.email = params['email']
        else:
            self.email = 'UNCONFIRMED'

        # Playlists
        if 'playlists' in params.keys():
            self.playlists = params['playlists']
        else:
            self.playlists = []

        # Registration date
        if 'reg_date' in params.keys():
            self.reg_date = params['reg_date']
        else:
            self.reg_date = None
