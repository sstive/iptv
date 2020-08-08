
DB_tables = {
    'channels': 'CREATE TABLE channels(id SMALLINT unsigned AUTO_INCREMENT UNIQUE NOT NULL, name VARCHAR(150) UNIQUE NOT\
                 NULL, theme TINYINT unsigned NOT NULL DEFAULT 0, sd TEXT,hd TEXT,fhd TEXT,qhd TEXT,uhd TEXT, PRIMARY KEY(id));',
    'playlists_forms': 'CREATE TABLE playlists_forms (id SMALLINT unsigned NOT NULL UNIQUE AUTO_INCREMENT, name VARCHAR(15) UNIQUE\
                 NOT NULL, channels TEXT, quality TINYINT unsigned NOT NULL DEFAULT 1, PRIMARY KEY(id))',
    'sources': 'CREATE TABLE sources(id SMALLINT unsigned NOT NULL UNIQUE AUTO_INCREMENT, url TEXT NOT NULL, protocol\
                 TINYINT unsigned NOT NULL DEFAULT 0, channels SMALLINT unsigned NOT NULL DEFAULT 0, ch_available \
                 SMALLINT unsigned NOT NULL DEFAULT 0, unavailable TINYINT unsigned NOT NULL DEFAULT 0,PRIMARY KEY(id))',
    'playlists': 'CREATE TABLE playlists (id SMALLINT unsigned NOT NULL UNIQUE, data TEXT, PRIMARY KEY(id))'
}
