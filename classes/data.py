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

protocols = [
    'http',
    'https',
    'ftp',
    'sftp'
]

Qualities = [
    # SD (PAL)
    [
        'sd',
        '(sd)',
        '[sd]',
        'pal',
        '(pal)',
        '[pal]',
        '480p',
        '[480p]',
        '(480p)'
     ],
    # HD (720p)
    [
        'hd',
        '[hd]',
        '(hd)',
        '720p',
        '[720p]',
        '(720p)'
    ],
    # FHD (1080p)
    [
        'fhd',
        '[fhd]',
        '(fhd)',
        '1080p',
        '[1080p]',
        '(1080p)'
    ],
    # QHD (2k)
    [
        'qhd',
        '[qhd]',
        '(qhd)',
        '2k',
        '[2k]',
        '(2k)',
        '1440p',
        '[1440p]',
        '(1440p)'
    ],
    # UHD (4k)
    [
        'uhd',
        '[uhd]',
        '(uhd)',
        '4k',
        '[4k]',
        '(4k)'
    ]
]

themes = [
    # Business
    ['рбк', 'cc 2', 'cc 3', 'cnbc', 'cnbc asia', 'cnbc europe', ],

    # Kids
    ['4kids', '4multimania', 'балапан', 'бибигон', 'детский мир', 'карусель', 'мульт', 'пиксель', 'радость моя',
     'стс kids', 'плюсплюс', 'тлум hd', 'boomerang', 'canal j', 'cartoon network', 'disney channel', 'disney cinemagic',
     'disney junior', 'disney xd', 'fox kids', 'gulli', 'jetix', 'jimjam', 'kids station', 'kika', 'lâle',
     'nickelodeon', 'nicktoons', 'spacetoon', 'super rtl', 'super7', 'teenick', 'teletoon', 'tiji', 'toon disney',
     'land', ],

    # Info
    ['а1+', 'астрахань 24', 'беларусь 24', 'вместе рф', 'коммерсантъ', 'москва 24', 'рбк', 'россия 24',
     'телеканал 16/12', 'урфо 24', 'хабар 24', 'царьград', 'эксперт', 'armnews', 'cgtn', 'channel newsasia', 'cnbc',
     'cnbc asia', 'cnbc europe', 'cnn', 'cnn international', 'euronews', 'kazakh', 'life', 'msnbc', 'n', 'news7', 'n',
     'one news', 'polsat news', 'polsat news 2', 'polsat sport news', 'rt', 'rt español', 'rt uk', 'ta3', 'patriot',
     'nz 7', 'ubr', 'uzreport', 'welt', ],

    # Music
    ['9 волна', 'дар 21', 'лайм', 'м1', 'м2', 'ммс', 'муз', 'музыка первого', 'н плюс музыка', 'о2', 'планета',
     'тнт music', 'туркмен овазы', 'шахнавоз', 'a one', 'acb', 'clubbing', 'country music television', 'dancetrippin',
     'eu music', 'europa plus', 'fuse', 'hit', 'lux', 'mad', 'mcm', 'mezzo', 'mnet', 'm россия', 'm украина', 'm dance',
     'm europe', 'm live hd', 'm uk', 'muzzone', 'o', 'ru', 'trace urban', 'u', 'vh1', 'vh1 россия', 'viva',
     'viva polska', 'zor', ],

    # Parliament
    ['вместе рф', 'рада', 'собраниски канал', 'bbc parliament', 'phoenix', ],

    # Cognitive
    ['24 док', '365 дней', 'беларусь 2', 'беларусь 3', 'білім және мәдениет', 'война и мир', 'еда', 'кто есть кто',
     'мама', 'моя планета', 'наука', 'охотник и рыболов', 'приключения hd', 'психология 21', 'совершенно секретно',
     'техно 24', 'шогакат', 'animal planet', 'da vinci', 'discovery channel', 'discovery hd showcase',
     'discovery world', 'dr k', 'history channel', 'investigation discovery', 'kazakh', 'lux', 'nat geo wild',
     'national geographic', 'outdoor channel', 'rambler телесеть', 'russian travel guide', 'science channel',
     'the biography channel', 'viasat explore', 'yle teema', ],

    # Fun
    ['2x2', '31 канал', 'домашний', 'пятница!', 'синема', 'совершенно секретно', 'супер', 'тнт4', 'ю', 'a', 'canal j',
     'clubbing', 'diva universal', 'dr3', 'e!', 'fashion', 'kabel eins', 'lux', 'luxe', 'milliy', 'my5',
     'paramount channel', 'rtl zwei', 'sony sci fi', 'teenick', 'tlc', 'viva', 'zor', ],

    # Sport
    ['2 спорт 2', 'беларусь 2', 'беларусь 5', 'варзиш', 'ктрк спорт', 'кхл', 'матч премьер', 'матч', 'матч! арена',
     'матч! игра', 'матч! страна', 'матч! футбол 1', 'матч! футбол 2', 'матч! футбол 3', 'н плюс баскетбол',
     'н плюс спорт', 'н плюс спорт онлайн', 'н плюс спорт союз', 'н плюс теннис', 'н плюс nba',
     'олимпийская вещательная служба', 'планета спорт', 'реал мадрид', 'россия 2', 'семёрка', 'спартак',
     'список спортивных телеканалов мира', 'футбол', 'футбол 1', 'футбол 2', 'acb', 'bt sport', 'eurosport',
     'eurosport 1', 'eurosport 2', 'hd спорт', 'mu', 'nba', 'polsat sport', 'polsat sport extra', 'polsat sport news',
     'premier sports', 'ring', 'setanta sports', 'sky sport', 'sky sports', 'sport', 'sport7', 'turkmenistan sport',
     'uzreport', 'viasat sport', 'xsport', ],

    # Common
    ['la 1', '1 й канал останкино', '1+1', '2+2', '4 й канал останкино', '31 канал', 'армения 2', 'беларусь 1',
     'вторая программа цт', 'звезда', 'интер', 'ктк', 'македония', 'мир', 'московская программа цт',
     'московский телевизионный канал', 'н', 'н беларусь', 'нтн', 'онт', 'первая программа цт', 'первый канал «евразия»',
     'пятый канал', 'рен', 'россия 1', 'седьмой канал', 'си би эс', 'стб', 'с', 'с', 'таджикистан', 'сафина', 'центр',
     '6', 'і', 'с', 'тонис', 'украина', 'хабар', 'хазар', 'чеёртая программа цт', 'эра', 'alpha',
     'american broadcasting company', 'ant1', 'antena 3', 'asyl arna', 'az', 'canale 5', 'cuatro', 'diyor',
     'fox broadcasting company', 'gms', 'ic', 'i', 'jednotka', 'm6', 'mega channel', 'nbc', 'new greek', 'polsat',
     'public broadcasting service', 'qazaqstan', 'rtl television', 'sat 1', 'lasexta', 'sic', 'skai', 'telecinco',
     'tf1', 'the cw television network', 'nova', '3', '3', '4', 'vox', ],

    # Films
    ['кинопоказ', 'киносвидание', 'кинохит', 'комедийное', 'родное кино', 'русский иллюзион', 'синамо', 'синема',
     'супер', '3', 'телеклуб', 'diva universal', 'enter фильм', 'syfy universal', 'tcm', '1000', '1000 русское кино',
     'universal', 'rai movie', 'rai premium', 'one piece  большой куш', ],

    # Football
    ['матч премьер', 'матч! футбол 1', 'матч! футбол 2', 'матч! футбол 3', 'футбол', 'футбол', 'футбол 1', 'футбол 2',
     'futbol', ],


    # Humour
    ['тнт4', 'comedy central', 'comedy']
]

themes_names = [
    'Прочие',
    'Деловые',
    'Дети',
    'Информация',
    'Музыка',
    'Парламентские',
    'Познавательные',
    'Развлекательные',
    'Спорт',
    'Общие',
    'Фильмы',
    'Футбол',
    'Юмор'
]
