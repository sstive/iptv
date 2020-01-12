import pymysql
from updater.source import Source
from updater.channel import Channel
from updater.data import DB_host, DB_name, DB_pass, DB_user, DB_port, DB_tables, protocols
from updater.utils import Utils
from updater.playlist import Playlist


class Database:

    def __init__(self):
        if DB_port:
            self.con = pymysql.connect(
                host=DB_host,
                db=DB_name,
                user=DB_user,
                password=DB_pass,
                port=DB_port,
                cursorclass=pymysql.cursors.DictCursor
            )
        else:
            self.con = pymysql.connect(
                host=DB_host,
                db=DB_name,
                user=DB_user,
                password=DB_pass,
                cursorclass=pymysql.cursors.DictCursor
            )
        print('Connection with database started!')
        self.__check_tables__()

    def __del__(self):
        self.con.close()
        print('Connection with database closed!')

    @staticmethod
    def __format_response__(response, key):
        ret = []
        for s in response:
            ret.append(s[key])
        return ret

    @staticmethod
    def __db_to_channel__(db_data):
        name = Utils.to_eng(db_data['name'], True)
        channel = Channel(name, db_data['theme'], db_data['id'])

        # Adding urls to channel
        channel.add_str_urls(db_data['sd'], 0)
        channel.add_str_urls(db_data['hd'], 1)
        channel.add_str_urls(db_data['fhd'], 2)
        channel.add_str_urls(db_data['uhd'], 3)

        return channel

    def __check_tables__(self):
        print('Checking tables in database...')

        with self.con.cursor() as cur:
            # Getting tables
            cur.execute('SHOW TABLES')

            # Existing tables in database
            tables = self.__format_response__(cur.fetchall(), f'Tables_in_{DB_name}')

            # Looking for missing tables
            for table in DB_tables:
                if table not in tables:
                    print(f'\tTable {table} not exists in database! Creating...')
                    cur.execute(DB_tables[table])

        print('Database checked!')

    def add_source(self, source):
        print(f'Adding source {source.url} to database...')

        # Sources in database
        sources = self.get_sources('url')

        if source.url in sources:
            print('Source already exists!')
            return False

        with self.con.cursor() as cur:
            cur.execute(f'INSERT INTO sources (url, protocol) VALUES (\'{source.host}\', {source.protocol})')

        self.con.commit()
        print('Source added!')

    def get_sources(self, resp='sources'):
        print(f'Getting sources from database...')

        # Output
        sources = []

        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM sources')
            src = cur.fetchall()

        for args in src:
            if resp == 'url':
                sources.append(protocols[args['protocol']] + '://' + args['url'])
            else:
                sources.append(Source(id=args['id'], protocol=args['protocol'], host=args['url'], unavailable=args['unavailable']))

        print('Sources received!')
        return sources

    def update_sources(self, sources):
        print('Updating sources...', end=' ')

        for src in sources:
            with self.con.cursor() as cur:
                cur.execute(f'UPDATE sources SET channels={src.channels}, ch_available={src.ch_available}, unavailable={src.unavailable} WHERE id={src.id}')
                cur.execute('DELETE FROM sources WHERE unavailable >= 10 OR ch_available < 5')

        self.con.commit()
        print('Done!')

    def add_channels(self, channels):
        print(f'Adding {len(channels)} channels to database...', end=' ')
        for ch in channels.values():
            with self.con.cursor() as cur:
                cur.execute(f'INSERT INTO channels (name, theme, sd, hd, fhd, uhd) VALUES (\'{ch.label}\', {ch.theme}, '
                            f'"{ch.get_str_urls(0)}", "{ch.get_str_urls(1)}", "{ch.get_str_urls(2)}", '
                            f'"{ch.get_str_urls(4)}") ON DUPLICATE KEY UPDATE name=\'{ch.label}\', theme={ch.theme}, '
                            f'sd="{ch.get_str_urls(0)}", hd="{ch.get_str_urls(1)}", '
                            f'fhd="{ch.get_str_urls(2)}", uhd="{ch.get_str_urls(3)}"')
            self.con.commit()
        print('Done!')

    def get_channels(self):
        channels = {}

        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM channels')
            chs = cur.fetchall()

        for ch in chs:
            name = Utils.to_eng(ch['name'], True)
            channels[name] = self.__db_to_channel__(ch)

        return channels

    def get_channel(self, **params):
        with self.con.cursor() as cur:
            if 'id' in params.keys():
                cur.execute(f'SELECT * FROM channels WHERE id = {params["id"]}')
            elif 'name' in params.keys():
                cur.execute(f'SELECT * FROM channels WHERE name = \'{params["name"]}\'')
            else:
                return None
            return self.__db_to_channel__(cur.fetchone())

    def get_playlists(self):
        playlists = []
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM playlists')
            for pl in cur.fetchall():
                playlists.append(Playlist(pl['name'], pl['quality'], pl['channels'].split(',')))

        return playlists
