import urllib
import urllib.request
from urllib.error import URLError


def get(url, timeout=5, err_resp=False):
    print(f'Getting url: {url}')
    try:
        return urllib.request.urlopen(url, timeout=timeout).read().decode('utf-8')
    except URLError as err:
        print(f'\t{err}: {url}\n')
        return err_resp
    except Exception as e:
        print(f'\t{e}: {url}\n')
        return err_resp


def check_connection(url):
    try:
        if urllib.request.urlopen(url, timeout=3).getcode() == 200:
            return True
        return False
    except URLError as err:
        print(f'\t{err}: {url}')
        return False
    except Exception as e:
        print(f'\t{e}: {url}')
        return False


def to_eng(text, decode=False):
    letters = {
        # Lowercase
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': '$0', 'ж': '$1', 'з': 'z', 'и': 'i',
        'й': '$2', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': '$3', 'ч': '$4', 'ш': '$5', 'щ': '$6', 'ь': '$7', 'ы': '$8',
        'ъ': '$9', 'э': '@0', 'ю': '@1', 'я': '@2',
        # Uppercase
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': '~0', 'Ж': '~1', 'З': 'Z', 'И': 'I',
        'Й': '~2', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': '~3', 'Ч': '~4', 'Ш': '~5', 'Щ': '~6', 'Ь': '~7', 'Ы': '~8', 'Ъ': '~9',
        'Э': '%0', 'Ю': '%1', 'Я': '%2'
    }

    new = []

    if decode:
        for k, v in letters.items():
            text = text.replace('^' + v, k)
        return text

    for s in text:
        if s in letters.keys():
            new.append('^' + letters[s])
        else:
            new.append(s)
    return ''.join(new)


def prepare_to_compare(text):
    return text.lower().replace('-', ' ').replace('.', '').replace('tv', '').replace('тв', '').replace('_', ' ').replace('#', '').replace('=', '').replace('!', '').replace('?', '').strip()
