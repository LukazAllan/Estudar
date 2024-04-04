# Python 3.12
"""
param log: logging module,
param data: load file
param d:
param j:
param r:
param r2:
param q:
Δθλ¹²³⁰⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉⁺⁻⁽⁾"""
from logging import Logger
import canivete
import json
import logging
import os
import os.path as path
from random import randint
from canivete import limpa, cor
"""class ArquivoJsonErro(Exception):
    def __init__(self,msg):
        self.msg(msg)"""

arquivo = 'base'
logging.basicConfig(filename=f'{arquivo}.py.log', filemode='w', encoding='utf-8', format='%(asctime)s %(levelname)s - %(message)s',
                    level=logging.DEBUG)
log: Logger = logging.getLogger()
log.debug('__init__')

if not path.isfile(f'{arquivo}.json'):
    log.critical('O arquivo não foi carregado')
    print('O arquivo não foi carregado')
    pass
else:
    with open(f'{arquivo}.json', 'r', encoding='utf-8') as file:
        data = dict(json.load(file))
        # except:
        # raise ArquivoJsonErro
        file.close()
    log.debug('loading...')
    j = {'p': 0, 'r': 0}
    while True:
        limpa()
        log.debug(f"rodada {j['r']}")
        j['r'] += 1
        caminho = data
        ra = ''
        for c in range(10):
            #input(caminho)
            if type(caminho) == dict:
                escolha = randint(0, len(list(caminho.keys())) - 1)
                if c == 0:
                    rm = list(caminho.keys())[escolha].lower()
                if c > 0:
                    ra = ra + f'{list(caminho.keys())[escolha]}'
                caminho = caminho[list(caminho.keys())[escolha]]
            else:
                d: object = caminho[randint(0, len(caminho) - 1)].copy()
                break

        # rm = list(data.keys())[randint(0, len(list(data.keys()))-1)]
        # log.info(f'rm = {rm}')
        # ra = list(data[rm].keys())[randint(0, len(list(data[rm].keys()))-1)]
        # log.info(f'ra = {ra}')
        # d = data[rm][ra]
        # input(d)
        q = None
        print(f'rod: {j["r"]}  pto: {j["p"]}\nsobre {rm} em {ra}:')
        log.info(f'0={d[0]} 1={d[1]}, ')
        sl = randint(0, len(d[1]) - 1)
        if type(d[1]) == list:
            log.info(f'd[1][sl] = {d[1][sl]}')
            while not q or q == '':
                q = input(f'{cor(rm)}{d[1][sl]}{cor()} ')
            log.info(f'STDIN: input\nrod: {j["r"]}  pto: {j["p"]}\nsobre {rm} em {ra}:\n{d[1][sl]}')
        elif type(d[1]) == str:
            while not q or q == '':
                q = input(f'{cor(rm)}{d[1]}{cor()} ')
            log.info(f'STDIN: input\nrod: {j["r"]}  pto: {j["p"]}\nsobre {rm} em {ra}:\n{d[1]}')

        print(canivete.semacento(q), canivete.semacento(d[0]))
        if type(d[0]) == str and canivete.semacento(q) == canivete.semacento(d[0]):
            print('Certa resposta')
            j['p'] += 1
            log.info('str and certo')
            log.info(f'True \'{q}\' == \'{d[0]}\'')
        elif type(d[0]) == list and canivete.semacento(q) in canivete.semacento(d[0]):
            print('Certa resposta')
            j['p'] += 1
            log.info('list and certo')
            log.info(f'True \'{q}\' == \'{d[0]}\'')
        else:
            print(f'Incorreto.\nA resposta era {d[0]}')
            log.info('errado')
            log.info(f'False \'{q}\' != \'{d[0]}\'')
        w = input('sair? ')
        if not w == '':
            break
