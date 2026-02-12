from json import load, dump
from canivete import *
import questionary

BASE = 'base.json'
ENCODING = "utf-8"

class Editor:
    def __init__(self):
        self.load_base()
        self.run()
    
    def load_base(self):
        global BASE, ENCODING
        with open(BASE, encoding=ENCODING) as f:
            self.base: dict = dict(load(f))
            self.materias = list(self.base.keys())
    
    def save_base(self):
        global BASE, ENCODING
        with open(BASE, 'w', encoding=ENCODING) as f:
            dump(self.base, f, indent=4, ensure_ascii=False)
    
    def menu_principal(self):
        cls()
        print(f'>/')
        print("-=" * 30)
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^60}')
        print("-=" * 30)
        for materia in self.materias:
            print(f' {materia} ', end="|")
        print()
        print("-=" * 30)
        questionary.print("Escolha uma opção para começar:", style="fg:cyan")
        escolha = questionary.select(
            "Opção:",
            choices=[
                "1. Navegar em Matérias",
                "2. Adicionar Matéria",
                "3. Editar Nome de Matéria",
                "4. Remover Matéria",
                "0. Sair"
                ]
        ).ask()
        return escolha
    
    def selecionar_materia(self):
        cls()
        print(f'>/')
        print("-=" * 30)
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^60}')
        print(f'{"Seleção de Matéria":^60}')
        print("-=" * 30)
        questionary.print("Escolha uma matéria para editar:", style="fg:cyan")
        escolha = questionary.select(
            "Matéria:",
            choices= self.materias + ["0"]
        ).ask()
        return escolha
    
    def menu_materia(self, materia):
        cls()
        print(f'>/{materia}')
        print("-=" * 30)
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^60}')
        print("-=" * 30)
        for assunto in self.base[materia]:
            print(f' {assunto} ', end="|")
        print()
        print("-=" * 30)
        questionary.print("Escolha uma opção para editar a matéria:", style="fg:cyan")
        escolha = questionary.select(
            "Opção:",
            choices=[
                "1. Navegar em Assuntos",
                "2. Adicionar Assunto",
                "3. Editar Nome de Assunto",
                "4. Remover Assunto",
                "0. Voltar"
                ]
        ).ask()
        return escolha
    
    def selecionar_assunto(self, materia):
        cls()
        print(f'>/{materia}')
        print("-=" * 30)
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^60}')
        print(f'{"Seleção de Assunto":^60}')
        print("-=" * 30)
        questionary.print("Escolha um assunto para editar:", style="fg:cyan")
        escolha = questionary.select(
            "Assunto:",
            choices= list(self.base[materia].keys()) + ["0"]
        ).ask()
        return escolha
    
    def menu_assunto(self, materia, assunto):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * 30)
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^60}')
        print("-=" * 30)
        questionary.print("Escolha uma opção para editar o assunto:", style="fg:cyan")
        escolha = questionary.select(
            "Opção:",
            choices=[
                "1. Exibir Nós",
                "2. Editar Nós",
                "0. Voltar"
                ]
        ).ask()
        return escolha
    
    def menu_editar_nos(self, materia, assunto):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * 30)
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^60}')
        print(f'{"Edição de Nós":^60}')
        print("-=" * 30)
        for no, num in self.base[materia][assunto]['nodes'].items():
            print(f' {no}:{num} ', end="|")
        print()
        print("-=" * 30)
        questionary.print("Escolha uma opção para editar os nós:", style="fg:cyan")
        escolha = questionary.select(
            "Opção:",
            choices=[
                "1. Adicionar Nó",
                "2. Editar Nó",
                "3. Remover Nó",
                "0. Voltar"
                ]
        ).ask()
        return escolha
    
    def escolher_no(self, materia, assunto):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * 30)
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^60}')
        print(f'{"Escolha de Nó":^60}')
        print("-=" * 30)
        questionary.print("Escolha um nó para editar:", style="fg:cyan")
        escolha = questionary.select(
            "Nó:",
            choices= list(self.base[materia][assunto]['nodes'].keys()) + ["0"]
        ).ask()
        return escolha
    
    def adicionar_no(self, materia, assunto, no):
        pass

    def editar_no(self, materia, assunto, no):
        pass

    def remover_no(self, materia, assunto, no):
        pass
    
    def exibe_nos(self, materia, assunto):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * 30)
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^60}')
        print(f'{"Exibição de Nós":^60}')
        print("-=" * 30)
        for no, num in self.base[materia][assunto]['nodes'].items():
            print(f' {no}:{num} ', end="|")
        print()
        print("-=" * 30)
        questionary.print("Pressione Enter para continuar...", style="fg:cyan")
        input()
    
    def run(self):
         while True:
            MP = self.menu_principal()
            match MP:
                case "1. Navegar em Matérias":
                    a_materia = self.selecionar_materia()
                    if a_materia == "0":
                        continue
                    while True:
                        MM = self.menu_materia(a_materia)
                        match MM:
                            case "1. Navegar em Assuntos":
                                o_assunto = self.selecionar_assunto(a_materia)
                                if o_assunto == "0":
                                    continue
                                while True:
                                    MA = self.menu_assunto(a_materia, o_assunto)
                                    match MA:
                                        case "1. Exibir Nós":
                                            self.exibe_nos(a_materia, o_assunto)
                                        case "2. Editar Nós":
                                            while True:
                                                ME = self.menu_editar_nos(a_materia, o_assunto)
                                                if ME == "0. Voltar":
                                                    break
                                                o_no = self.escolher_no(a_materia, o_assunto)
                                                match ME:
                                                    case "1. Adicionar Nó":
                                                        self.adicionar_no(a_materia, o_assunto,o_no)
                                                    case "2. Editar Nó":
                                                        self.editar_no(a_materia, o_assunto,o_no)
                                                    case "3. Remover Nó":
                                                        self.remover_no(a_materia, o_assunto,o_no)
                                        case "0. Voltar":
                                            break
                            case "0. Voltar":
                                break
                case "0. Sair":
                    #self.save_base()
                    break


if __name__ == "__main__":
    editor = Editor()