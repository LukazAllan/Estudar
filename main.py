import questionary
from random import randint, choice
from commentjson import load
from canivete import *
from typing import Final

BASE = 'base.json'

class Perguntas:
    def __init__(self):
        global BASE
        self.pontuacao = 0
        self.rodada = 1
        self.tema = ""
        self.subtema = ""
        
    def load_base(self):
        with open(BASE, encoding="utf-8") as f:
            self.base: Final[dict] = dict(load(f))
            self.temas = list(self.base.keys())
            self.subtemas = {tema: list(self.base[tema].keys()) for tema in self.temas}

    def clean(self):
        self.tema = ""
        self.subtema = ""

    def menu(self):
        self.load_base()
        cls()
        print("-=" * 30)
        print(f'{"JOGO DE PERGUNTAS E RESPOSTAS":^60}')
        print(f'{"Menu Principal":^60}')
        print("-=" * 30)
        print("1. Jogar com TODO o conteúdo")
        print("2. Jogar por Matéria")
        print("3. Jogar por Assunto")
        print("0. Sair")
        print("-=" * 30)
        questionary.print("Escolha uma opção para começar:", style="fg:cyan")
        escolha = questionary.select(
            "Opção:",
            choices=[
                "1","2","3","0"
            ]
        ).ask()
        return escolha
    
    def menu_materia(self):
        cls()
        print("-=" * 30)
        print(f'{"JOGO DE PERGUNTAS E RESPOSTAS":^60}')
        print(f'{"Menu por Matéria":^60}')
        print("-=" * 30)
        questionary.print("Escolha uma matéria para jogar:", style="fg:cyan")
        escolha = questionary.select(
            "Matéria:",
            choices= self.temas + ["0"]
        ).ask()
        return escolha
    
    def menu_assunto(self, materia):
        cls()
        print("-=" * 30)
        print(f'{"JOGO DE PERGUNTAS E RESPOSTAS":^60}')
        print(f'{"Menu por Assunto":^60}')
        print("-=" * 30)
        questionary.print("Escolha um assunto para jogar:", style="fg:cyan")
        escolha = questionary.select(
            "Assunto:",
            choices= self.subtemas[materia] + ["0"]
        ).ask()
        return escolha

    def mostrar_titulo(self):
        cls()
        print("🎯" * 30)
        print(f'{"JOGO DE PERGUNTAS E RESPOSTAS":^60}')
        print("🎯" * 30)
        print(f"📊 Rodada: {self.rodada}")
        print(f"✅ Acertos: {self.pontuacao}/{self.rodada - 1}")
        print(f"Matéria: {self.tema:<10} | Assunto: {self.subtema.capitalize()}")
        print()

    def escolher_pergunta(self, materia=None, assunto=None):
        if materia is not None:
            area = materia
        else:
            area = choice(list(self.base.keys()))
        
        if assunto is not None:
            sub = assunto
        else:
            sub = choice(list(self.base[area].keys()))
        self.tema = area
        self.subtema = sub

        data = self.base[area][sub]
        
        escolha = choice(data["edges"])
        id_pergunta = escolha[0] # pergunta é sempre a origem ou escolha[0]

        for p, id in data["nodes"].items():
            if id == id_pergunta:
                pergunta = p
                break
    
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
        questionary.print(questao['pergunta'] + "\n", style='fg:yellow')
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
    
    def new_run(self):
        while True:
            menu = self.menu()
            match menu:
                case "1":
                    materia = None
                    assunto = None
                case "2":
                    materia = self.menu_materia()
                    if materia == "0":
                        continue
                    assunto = None
                case "3":
                    materia = self.menu_materia()
                    if materia == "0":
                        continue
                    assunto = self.menu_assunto(materia)
                    if assunto == "0":
                        continue
                case "0":
                    break
            
            while True:
                P = self.escolher_pergunta(materia, assunto)
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

if __name__ == '__main__':
    jogo = Perguntas()
    #jogo.run()
    jogo.new_run()
