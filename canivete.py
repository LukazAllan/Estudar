# Python 3.10+
from os import path, system, name

def tit(txt):
    t = int(len(txt) + 8)
    print('-' * t)
    print(f'{txt:^{t}}')
    print('-' * t)


def semacento(st):
    #print("tô aq")
    s = None
    if type(st) == str:
        s = list(st)
    else:
        s = st.copy()
    for c in range(0,len(s)):
        s[c] = s[c].lower()
        if 'é' in s[c]:
            #print('achei é')
            s[c] = s[c].replace('é','e')
        if 'ê' in s[c]:
            #print('achei ê')
            s[c] = s[c].replace('é','e')
        if 'á' in s[c]:
            #print('achei á')
            s[c] = s[c].replace('á','a')
        if 'ã' in s[c]:
            #print('achei ã')
            s[c] = s[c].replace('ã','a')
        if 'â' in s[c]:
            #print('achei é')
            s[c] = s[c].replace('â','a')
        if 'í' in s[c]:
            #print('achei í')
            s[c] = s[c].replace('í','i')
        if 'ó' in s[c]:
            #print('achei ó')
            s[c] = s[c].replace('ó','o')
        if 'ô' in s[c]:
            #print('achei ô')
            s[c] = s[c].replace('ô','o')
        if 'õ' in s[c]:
            #print('achei ó')
            s[c] = s[c].replace('õ','o')
        if 'ú' in s[c]:
            #print('achei ú')
            s[c] = s[c].replace('ú','u')
        if 'ç' in s[c]:
            #print('achei ç')
            s[c] = s[c].replace('ç','c')
    if type(st) == str:
        return ''.join(s)
    else:
        return s


def cor(md=None):
    dic={
    	None:'\033[m',
    	'química':'\033[1;35;43m',
    	'biologia':'\033[1;32;43m',
    	'física':'\033[1;36;43m',
    	
    	'matemática':'\033[1;33;44m',
    	
    	'história':'\033[1;34;44m',
    	'geografia' :'\033[1;34;44m',
    	'filosofia':'\033[1;34;44m',
    	'sociologia':'\033[1;34;44m',
    	
    	'gramática':'\033[1;36;41m',
    	'literatura':'\033[1;36;41m'
    }
    try:
        return dic[md]
    except:
        return ''


def cls():
    if name == 'nt':
            system('cls')
    else:
        system('clear')
    


def limpa():
    """
    Função que limpa a tela
    """
    if path.isdir('C:/'):
        system('cls')
    if path.isdir('/storage/emulated/0/'):
        system('clear')


# noinspection PyArgumentList
def linque(caminho, form='r', asci=True):
    """
    Função que linca o arquivo
    :type asci: bool
    :type form: object
    :param caminho: indica o caminho do arquivo
    :param asci: leitura de códigos ascii, que
    para ativar escreva False para ele
    :return: a
    """
    if path.isfile(caminho, form):
        return open(caminho, form, ensure_ascii=asci)


def pc():
    if path.isdir('C:/'):
        return 'windows'
    elif path.isdir('/storage/emulated/0/'):
        return 'android/linux'


def rinput(texto: object, b: object = None, enfeite: object = ':', errormsg = 'Tente novamente.'):
    """
    Função que não para de executar input
    até que você digite alguma coisa ou
    digite a coisa correta.
    :type texto: object
    :param texto: Exibe no input
    :type b: object
    :param b: lista de condição
    :return: var c
    """
    if b is None:
        b = False
    cont = -1
    while True:
        cont += 1
        if cont == 0:
            c = input(f'{texto}{enfeite} ')
        else:
            c = input(f'{errormsg}\n{texto}{enfeite} ')
        if c == '':
            limpa()
            pass
        else:
            if not b:
                return str(c)
            else:
                if c in b:
                    return str(c)
                else:
                    pass
