import questionary
from random import randint, choice
from json import load
from canivete import *
from typing import Final

class Perguntas:
    def __init__(self):
        self.pontuacao = 0
        self.rodada = 1
        self.tema = ""
        self.subtema = ""
        
        with open("base.json", encoding="utf-8") as f:
            self.base: Final[dict] = dict(load(f))

    def clean(self):
        self.tema = ""
        self.subtema = ""

    def mostrar_titulo(self):
        cls()
        print("🎯" * 20)
        print("    JOGO DE PERGUNTAS E RESPOSTAS")
        print("🎯" * 20)
        print(f"📊 Rodada: {self.rodada}")
        print(f"✅ Acertos: {self.pontuacao}/{self.rodada - 1}")
        print(f"Matéria: {self.tema:<10} | Assunto: {self.subtema.capitalize()}")
        print()

    def escolher_pergunta(self):
        # escolhendo a pergunta
        area_do_conhecimento = list(self.base.keys())
        aleatorio_tema = randint(0, len(area_do_conhecimento)-1)
        self.tema = area_do_conhecimento[aleatorio_tema]

        sub_area = list(self.base[self.tema].keys())
        aleatorio_subtema = randint(0, len(sub_area)-1)
        self.subtema = sub_area[aleatorio_subtema]

        #Ponto de Interesse
        pi = choice(
            self.base[self.tema][self.subtema].copy()
        )
        # escolha do lado e da pergunta
        lado = choice([1, 0])
        if type(pi[lado]) == list:
            return {
                'pergunta': choice(pi[lado]),
                'resposta': pi[int(not lado)]
            }
        else:
            return {
                'pergunta': pi[lado],
                'resposta': pi[int(not lado)]
            }

    def resposta_certa(self):
        questionary.print("✅ CORRETO!", style="fg:green")
        
    def resposta_errada(self, questao):
        questionary.print(f"❌ ERRADO! A resposta correta era: {questao['resposta'] }", style="fg:red")

    def validar_pergunta(self,resposta, questao):
        if type(questao['resposta']) == str and \
            semacento(resposta) == semacento(questao['resposta']):

            self.pontuacao += 1
            #self.resposta_certa()
            return True
            
        else: # type(questao['resposta']) == list:
            for R in questao['resposta']:
                if semacento(resposta) == semacento(questao['resposta']):
                    self.pontuacao += 1
                    #self.resposta_certa()
                    return True
        #self.resposta_errada()
        return False
            
        
        
    def perguntar(self, questao:list):
        questionary.print(questao['pergunta'], style='fg:yellow')
        q = False
        while not q or q == '':
            q = questionary.text(f'Sua Resposta ').ask()
        return q

        

    def run(self):
        while True:
            P = self.escolher_pergunta()
            self.mostrar_titulo()
            esta_correto = self.validar_pergunta(self.perguntar(P), P)
            self.mostrar_titulo()
            if esta_correto:
                self.resposta_certa()
            else:
                self.resposta_errada(P)
            exit = questionary.text("Vai sair, meu nobre?", qmark="◀").ask()

            if exit:
                break
            self.rodada +=1
            self.clean()

if __name__ == '__main__':
    jogo = Perguntas()
    jogo.run()
