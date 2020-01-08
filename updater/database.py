import pymysql
from source import Source
from channel import Channel
from data import DB_host, DB_name, DB_pass, DB_user, DB_port, DB_tables, protocols
from utils import Utils
from playlist import Playlist


class Database:

    def __init__(self):
        self.con = pymysql.connect(
            host=DB_host,
            db=DB_name,
            user=DB_user,
            password=DB_pass,
            port=DB_port,
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
            cur.execute(f'INSERT INTO sources (url, protocol) VALUES ({source.host}, {source.protocol})')

        self.con.commit()
        print('Source added!')

    def get_sources(self, resp='sources'):
        print(f'Getting sources from database...')

        # Output
        sources = []

        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM sources')
            src = cur.fetchall()

        for s in src:
            if resp == 'url':
                sources.append(protocols[s['protocol']] + '://' + s['url'])
            else:
                sources.append(Source(s['id'], s['protocol'], s['url']))

        print('Sources received!')
        return sources

    def update_sources(self, sources):
        if len(sources) == 0:
            return 0

        bad_count = 0

        # TODO: Refactor Adding
        print('Updating sources...', end=' ')
        inc = 'UPDATE sources SET unavailable = unavailable + 1 WHERE '
        res = 'UPDATE sources SET unavailable = 0 WHERE '

        for src in sources:
            with self.con.cursor() as cur:
                cur.execute(f'UPDATE sources SET channels={src.channels}, ch_available={src.ch_available} WHERE id={src.id}')
            self.con.commit()
            if src.ch_available < 20 or not src.src_available:
                inc += f'id = {src.id} OR '
                res += f'(NOT id = {src.id}) AND '
                bad_count += 1

        inc = inc[0: -4]
        res = res[0: -5]

        with self.con.cursor() as cur:
            if bad_count > 0:
                cur.execute(inc)
                cur.execute(res)
            cur.execute('DELETE FROM sources WHERE unavailable >= 10')
            # cur.execute('DELETE FROM sources WHERE ch_available < 5')
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
            channel = Channel(name, ch['theme'], ch['id'])

            channel.add_str_urls(ch['sd'], 0)
            channel.add_str_urls(ch['hd'], 1)
            channel.add_str_urls(ch['fhd'], 2)
            channel.add_str_urls(ch['uhd'], 3)

            channels[name] = channel
        return channels

    def get_playlists(self):
        playlists = []
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM playlists')
            for pl in cur.fetchall():
                playlists.append(Playlist(pl['name'], pl['quality'], pl['channels'].split(',')))

        return playlists
