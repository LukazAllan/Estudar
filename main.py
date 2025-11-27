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
        
        with open("base_grafo.json", encoding="utf-8") as f:
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
        area = choice(list(self.base.keys()))
        sub = choice(list(self.base[area].keys()))
        self.tema = area
        self.subtema = sub
    
        data = self.base[area][sub]
    
        nodes = list(data["nodes"].keys())
        pergunta = choice(nodes)
    
        id_pergunta = data["nodes"][pergunta]
    
        respostas_validas = [
            destino
            for origem, destino in data["edges"]
            if origem == id_pergunta
        ]
    
        # converter ids de volta para texto
        respostas_texto = [
            node for node, nid in data["nodes"].items() if nid in respostas_validas
        ]
    
        return {
            "pergunta": pergunta,
            "respostas": respostas_texto
        }
    
    def resposta_certa(self):
        questionary.print("✅ CORRETO!", style="fg:green")
        
    def resposta_errada(self, questao):
        corretas = " | ".join(questao["respostas"])
        questionary.print(f"❌ ERRADO! Respostas possíveis: {corretas}", style="fg:red")

    def validar_pergunta(self, resposta, questao):
            for r in questao["respostas"]:
                if semacento(resposta) == semacento(r):
                    self.pontuacao += 1
                    return True
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
