import os
import pymysql
from updater.source import Source
from updater.channel import Channel
from updater.data import DB_tables, protocols
from updater.playlist import Playlist


class Database:

    def __init__(self, from_web=False):
        if 'DB_PORT' in os.environ.keys():
            self.con = pymysql.connect(
                host=os.environ['DB_HOST'],
                db=os.environ['DB_DATABASE'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
                port=os.environ['DB_PORT'],
                cursorclass=pymysql.cursors.DictCursor
            )
        else:
            self.con = pymysql.connect(
                host=os.environ['DB_HOST'],
                db=os.environ['DB_DATABASE'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
                cursorclass=pymysql.cursors.DictCursor
            )
        print('\nConnection with database started!')

        if not from_web:
            self.__drop_database__()
            self.__check_tables__()

    def __del__(self):
        self.con.close()
        print('\nConnection with database closed!')

    @staticmethod
    def __format_response__(response, key):
        ret = []
        for s in response:
            ret.append(s[key])
        return ret

    @staticmethod
    def __db_to_channel__(db_data):

        name = db_data['name']

        channel = Channel(name, db_data['theme'], db_data['id'])

        # Adding urls to channel
        channel.add_str_urls(db_data['sd'], 0)
        channel.add_str_urls(db_data['hd'], 1)
        channel.add_str_urls(db_data['fhd'], 2)
        channel.add_str_urls(db_data['qhd'], 3)
        channel.add_str_urls(db_data['uhd'], 4)

        return channel

    def __drop_database__(self):
        if 'DROP_DATABASE' in os.environ.keys():
            print('\nAre you sure want to drop database? (y/n)')
            if input().lower() != 'y':
                return

            print('Dropping tables...')

            with self.con.cursor() as cur:
                cur.execute('SHOW TABLES')
                tables = self.__format_response__(cur.fetchall(), f"Tables_in_{os.environ['DB_DATABASE']}")

                for table in tables:
                    print(f'\t{table}...', end=' ')
                    cur.execute(f'DROP TABLE {table};')
                    print(f'Done!')
            self.con.commit()
            print('Done!')

    def __check_tables__(self):
        print('Checking tables in database...')

        with self.con.cursor() as cur:
            # Getting tables
            cur.execute('SHOW TABLES')

            # Existing tables in database
            tables = self.__format_response__(cur.fetchall(), f"Tables_in_{os.environ['DB_DATABASE']}")

            # Looking for missing tables
            for table in DB_tables:
                if table not in tables:
                    print(f'\tTable {table} not exists in database! Creating...', end=' ')
                    cur.execute(DB_tables[table])
                    print('Done!')

            if 'playlists_forms' not in tables:
                print('Adding default playlist')
                cur.execute('INSERT INTO playlists_forms (name, channels, quality) VALUES (\'Chizhov\', \
"Первый канал,Россия 1,МАТЧ!,НТВ,Пятый канал,Россия К,ТВ Центр,КАРУСЕЛЬ,Россия 24,ОТР,РЕН ТВ,Спас,СТС,Домашний,ТВ-3,ПЯТНИЦА!,Звезда,Мир,ТНТ,МУЗ ТВ", 2)')
            self.con.commit()

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
                cur.execute(f'INSERT INTO channels (name, theme, sd, hd, fhd, qhd, uhd) VALUES (\'{ch.label}\', {ch.theme},\
                    "{ch.get_str_urls(0)}", "{ch.get_str_urls(1)}", "{ch.get_str_urls(2)}", "{ch.get_str_urls(3)}", "{ch.get_str_urls(4)}"\
                    ) ON DUPLICATE KEY UPDATE name=\'{ch.label}\', theme={ch.theme}, sd="{ch.get_str_urls(0)}",\
                    hd="{ch.get_str_urls(1)}", fhd="{ch.get_str_urls(2)}", qhd="{ch.get_str_urls(3)}", uhd="{ch.get_str_urls(4)}"')
            self.con.commit()
        print('Done!')

    def get_channels(self):
        channels = {}
        # TODO: add checker
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM channels')
            chs = cur.fetchall()

        for ch in chs:
            name = ch['name']
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

    def get_playlists_forms(self):
        forms = []
        with self.con.cursor() as cur:
            cur.execute('SELECT * FROM playlists_forms')
            for pl in cur.fetchall():
                forms.append(Playlist(pl['id'], pl['name'], pl['quality'], list(map(str.strip, pl['channels'].split(',')))))
        return forms

    def save_playlist(self, id, data):
        with self.con.cursor() as cur:
            cur.execute(f'INSERT INTO playlists (id, data) VALUES ({id}, "{data}") ON DUPLICATE KEY UPDATE data="{data}"')
        self.con.commit()

    def get_playlist(self, **params):
        if 'id' not in params.keys():
            return 404

        with self.con.cursor() as cur:
            cur.execute(f"SELECT * FROM playlists WHERE id = {params['id']}")
            result = cur.fetchone()
        return result['data']
