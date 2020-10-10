def replace_symbols(s: str, *chars):
    for char in chars:
        if type(char) is tuple:
            s = s.replace(char[0], char[1])
        elif type(char) is str:
            s = s.replace(char, '')
    return s


def fix_theme(theme):
    if len(theme) < 3:
        return None

    theme = theme.strip()

    # Theme must contain at least 50% of russian symbols
    rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    theme_check = theme.replace(' ', '').lower()
    if list(map(lambda s: s in rus, theme_check)).count(True) / len(theme_check) < 0.5:
        return None

    return replace_symbols(theme, ('-', ' '), ('_', ' '))
