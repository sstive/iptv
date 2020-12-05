import urllib.request
from .parser import get_chunks


def replace_symbols(s: str, *chars):
    for char in chars:
        if type(char) is tuple:
            s = s.replace(char[0], char[1])
        elif type(char) is str:
            s = s.replace(char, '')
    return s


def fix_theme(theme):
    if len(theme) < 2:
        return None

    theme = theme.strip()

    # Theme must contain at least 50% of russian symbols
    rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    theme_check = theme.replace(' ', '').lower()
    if list(map(lambda s: s in rus, theme_check)).count(True) / len(theme_check) < 0.5:
        return None

    return replace_symbols(theme, ('-', ' '), ('_', ' '))


def check_url(url, recursion_level=0):
    if recursion_level > 3:
        return False

    try:
        req = urllib.request.urlopen(url, timeout=3)

        # Getting chunks urls, if this is not text file, we catch exception
        try:
            urls = get_chunks(req.read(10240).decode('UTF-8'))
        except UnicodeDecodeError:
            return True

        # If no urls in file or this is not m3u8
        if len(urls) == 0:
            return False

        # deleting some urls because too much of them
        while len(urls) > 20:
            i = 0
            while i < len(urls):
                del urls[i]
                i += 2

        # Checking chunks urls
        working = 0
        for chunk_url in urls:
            # By default checking_url equals to chunk_url
            checking_url = chunk_url

            # Chunk url may be not full (e.g. "/page1/something" or "chunk/1")
            parts = chunk_url.split('/')
            # If chunk url /foo/bar
            if parts[0] == '':
                checking_url = '/'.join(url.split('/')[:3]) + chunk_url
            # If chunk url foo/bar
            elif ':' not in parts[0]:
                if url[-1] == '/':
                    checking_url = url + chunk_url
                else:
                    checking_url = url + '/' + chunk_url
            # Checking url
            if check_url(checking_url, recursion_level+1):
                working += 1

        # Less than 75% is ok
        if working / len(urls) < 0.75:
            return False

        # All urls is ok
        return True

    # If something went wrong
    except Exception:
        return False
