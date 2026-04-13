import os
import shutil
from os import system, name


def semacento(st):
    s = None
    if type(st) == str:
        s = list(st)
    else:
        s = st.copy()
    for c in range(0, len(s)):
        s[c] = s[c].lower()
        if 'é' in s[c]:
            s[c] = s[c].replace('é', 'e')
        if 'ê' in s[c]:
            s[c] = s[c].replace('ê', 'e')
        if 'á' in s[c]:
            s[c] = s[c].replace('á', 'a')
        if 'ã' in s[c]:
            s[c] = s[c].replace('ã', 'a')
        if 'â' in s[c]:
            s[c] = s[c].replace('â', 'a')
        if 'í' in s[c]:
            s[c] = s[c].replace('í', 'i')
        if 'ó' in s[c]:
            s[c] = s[c].replace('ó', 'o')
        if 'ô' in s[c]:
            s[c] = s[c].replace('ô', 'o')
        if 'õ' in s[c]:
            s[c] = s[c].replace('õ', 'o')
        if 'ú' in s[c]:
            s[c] = s[c].replace('ú', 'u')
        if 'ç' in s[c]:
            s[c] = s[c].replace('ç', 'c')
    if type(st) == str:
        return ''.join(s)
    else:
        return s


def cls():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current += (" " if current else "") + word
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def cor(md=None):
    dic = {
        None: '\033[m',
        'química': '\033[1;35;43m',
        'biologia': '\033[1;32;43m',
        'física': '\033[1;36;43m',
        'matemática': '\033[1;33;44m',
        'história': '\033[1;34;44m',
        'geografia': '\033[1;34;44m',
        'filosofia': '\033[1;34;44m',
        'sociologia': '\033[1;34;44m',
        'gramática': '\033[1;36;41m',
        'literatura': '\033[1;36;41m'
    }
    try:
        return dic[md]
    except:
        return ''


def get_terminal_width() -> int:
    return shutil.get_terminal_size().columns