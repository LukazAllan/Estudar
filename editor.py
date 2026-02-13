from json import load, dump
# from canivete import cls
import questionary
from questionary import Choice
from os import get_terminal_size as gts, system, name as OSNAME

BASE = 'new_base.json'
#PREFIXO = "new_"
PREFIXO = ""
ENCODING = "utf-8"
TERMINAL_WIDTH = 60

def cls():
    global TERMINAL_WIDTH
    TERMINAL_WIDTH = gts().columns
    if OSNAME == 'nt':
        system('cls')
    else:
        system('clear')

def find_key_by_value(d, value):
    for key, val in d.items():
        if val == value:
            return key
    return None

class Editor:
    def __init__(self):
        self.SAIDA = "- SAIR -"
        self.load_base()
        self.run()
    
    def load_base(self):
        global BASE, ENCODING
        with open(BASE, encoding=ENCODING) as f:
            self.base: dict = dict(load(f))
            self.materias = list(self.base.keys())
    
    def save_base(self):
        global BASE, ENCODING, PREFIXO
        with open(PREFIXO+BASE, 'w', encoding=ENCODING) as f:
            dump(self.base, f, indent=4, ensure_ascii=False)
    
    def menu_principal(self):
        cls()
        print(f'>/')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        for materia in self.materias:
            print(f' {materia} ', end="|")
        print()
        print("-=" * (TERMINAL_WIDTH//2))
        questionary.print("Escolha uma opção para começar:", style="fg:cyan")
        escolha = questionary.select(
            "Opção:",
            choices=[
                "1. Navegar em Matérias",
                "2. Adicionar Matéria",
                "3. Editar Nome de Matéria",
                "4. Remover Matéria",
                "0. Sair e Salvar"
                ]
        ).ask()
        return escolha
    
    def selecionar_materia(self):
        cls()
        print(f'>/')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^{TERMINAL_WIDTH}}')
        print(f'{"Seleção de Matéria":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        if len(self.materias) == 0:
            questionary.print("Nenhuma matéria encontrada. Por favor, adicione uma matéria primeiro.", style="fg:red")
            input("Pressione ENTER para continuar...")
            return self.SAIDA
        elif len(self.materias) == 1:
            questionary.print(f"Única matéria encontrada: '{self.materias[0]}'. Selecionando automaticamente.", style="fg:green")
            input("Pressione ENTER para continuar...")
            return self.materias[0]
        questionary.print("Escolha uma matéria para editar:", style="fg:cyan")
        escolha = questionary.select(
            "Matéria:",
            choices= self.materias + [self.SAIDA]
        ).ask()
        return escolha
    
    def adicionar_materia(self):
        print(f'>/')
        print("-=" * (TERMINAL_WIDTH//2))
        while True:
            outra_materia = questionary.text("Qual o nome da nova matéria?").ask()
            escolha = questionary.confirm("Adicionar à base?").ask()
            if escolha:
                self.base[outra_materia] = {}
                questionary.print(f'Matéria {outra_materia} adicionado com sucesso!', style='fg:green')
            else:
                questionary.print("Skipping...", style="fg:red")
            input("Pressione ENTER para continuar...")

    def remover_materia(self, materia):
        cls()
        print(f'>/')
        print("-=" * (TERMINAL_WIDTH//2))
        if materia == self.SAIDA:
            questionary.print("Skipping...", style="fg:red")
            input("Pressione ENTER para continuar...")
            return 0
        escolha = questionary.confirm(f"Tem certeza que deseja remover a matéria '{materia}'? Isso também removerá todos os assuntos e nós associados a ela.", default=False).ask()
        if escolha:
            del self.base[materia]
            questionary.print(f'Matéria {materia} removida com sucesso!', style='fg:green')
            input("Pressione ENTER para continuar...")
            return 1
    
    def editar_nome_materia(self, materia):
        cls()
        print(f'>/')
        print("-=" * (TERMINAL_WIDTH//2))
        if materia == self.SAIDA:
            questionary.print("Skipping...", style="fg:red")
            input("Pressione ENTER para continuar...")
            return 0
        while True:
            questionary.print(f'Editar o nome de uma matéria poderá afetar sua posição dentro do dicionário.', style="fg:red")
            nova_materia = questionary.text("Digite o novo nome da matéria:").ask()
            if not nova_materia.strip():
                questionary.print("Nome inválido. Nenhum alteração foi feita.", style="fg:red")
                input("Pressione Enter para continuar...")
                continue
            break
        escolha = questionary.confirm(f"Tem certeza que deseja editar o nome da matéria '{materia}' para '{nova_materia}'? Isso também editará o nome de todos os assuntos e nós associados a ela.", default=False).ask()
        if escolha:
            self.base[nova_materia] = self.base.pop(materia)
            questionary.print(f'Matéria "{materia}" editada para "{nova_materia}" com sucesso!', style='fg:green')
        input("Pressione ENTER para continuar...")
        return 1

    
    def menu_materia(self, materia):
        cls()
        print(f'>/{materia}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        for assunto in self.base[materia]:
            print(f' {assunto} ', end="|")
        print()
        print("-=" * (TERMINAL_WIDTH//2))
        questionary.print("Escolha uma opção para editar a matéria:", style="fg:cyan")
        escolha = questionary.select(
            "Opção:",
            choices=[
                "1. Navegar em Assuntos",
                "2. Adicionar Assunto",
                "3. Editar Nome de Assunto",
                "4. Remover Assunto",
                self.SAIDA
                ]
        ).ask()
        return escolha

    def adicionar_assunto(self, materia):
        print(f'>/{materia}')
        print("-=" * (TERMINAL_WIDTH//2))
        while True:
            outro_assunto = questionary.text("Qual o nome do novo assunto?").ask()
            escolha = questionary.confirm("Adicionar à base?").ask()
            if escolha:
                self.base[materia][outro_assunto] = {"nodes": {}, "edges": []}
                questionary.print(f'Assunto {outro_assunto} adicionado com sucesso!', style='fg:green')
            else:
                questionary.print("Skipping...", style="fg:red")
            input("Pressione ENTER para continuar...")
    
    def editar_nome_assunto(self, materia, assunto):
        cls()
        print(f'>/{materia}')
        print("-=" * (TERMINAL_WIDTH//2))
        if assunto == self.SAIDA:
            questionary.print("Skipping...", style="fg:red")
            input("Pressione ENTER para continuar...")
            return 0
        while True:
            questionary.print(f'Editar o nome de um assunto poderá afetar sua posição dentro do dicionário.', style="fg:red")
            novo_assunto = questionary.text("Digite o novo nome do assunto:").ask()
            if not novo_assunto.strip():
                questionary.print("Nome inválido. Nenhum alteração foi feita.", style="fg:red")
                input("Pressione Enter para continuar...")
                continue
            break
        escolha = questionary.confirm(f"Tem certeza que deseja editar o nome do assunto '{assunto}' para '{novo_assunto}'? Isso também editará o nome de todos os nós associados a ele.", default=False).ask()
        if escolha:
            self.base[materia][novo_assunto] = self.base[materia].pop(assunto)
            questionary.print(f'Assunto "{assunto}" editado para "{novo_assunto}" com sucesso!', style='fg:green')
        input("Pressione ENTER para continuar...")
        return 1

    def remover_assunto(self, materia, assunto):
        cls()
        print(f'>/{materia}')
        print("-=" * (TERMINAL_WIDTH//2))
        if assunto == self.SAIDA:
            questionary.print("Skipping...", style="fg:red")
            input("Pressione ENTER para continuar...")
            return 0
        escolha = questionary.confirm(f"Tem certeza que deseja remover o assunto '{assunto}'? Isso também removerá todos os nós associados a ele.", default=False).ask()
        if escolha:
            del self.base[materia][assunto]
            questionary.print(f'Assunto {assunto} removido com sucesso!', style='fg:green')
            input("Pressione ENTER para continuar...")
            return 1
        questionary.print("Skipping...", style="fg:red")
        input("Pressione ENTER para continuar...")
        return 0
    
    def selecionar_assunto(self, materia):
        cls()
        print(f'>/{materia}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^{TERMINAL_WIDTH}}')
        print(f'{"Seleção de Assunto":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        if len(self.base[materia]) == 0:
            questionary.print("Nenhum assunto encontrado. Por favor, adicione um assunto primeiro.", style="fg:red")
            input("Pressione ENTER para continuar...")
            return self.SAIDA
        elif len(self.base[materia]) == 1:
            unica_chave = list(self.base[materia].keys())[0]
            questionary.print(f"Único assunto encontrado: '{unica_chave}'. Selecionando automaticamente.", style="fg:green")
            input("Pressione ENTER para continuar...")
            return unica_chave
        questionary.print("Escolha um assunto para editar:", style="fg:cyan")
        escolha = questionary.select(
            "Assunto:",
            choices= list(self.base[materia].keys()) + [self.SAIDA]
        ).ask()
        return escolha
    
    def menu_assunto(self, materia, assunto):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        questionary.print("Escolha uma opção para editar o assunto:", style="fg:cyan")
        escolha = questionary.select(
            "Opção:",
            choices=[
                "1. Exibir Nós",
                "2. Editar Nós",
                self.SAIDA
                ]
        ).ask()
        return escolha
    
    def menu_editar_nos(self, materia, assunto):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^{TERMINAL_WIDTH}}')
        print(f'{"Edição de Nós":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        for no, num in self.base[materia][assunto]['nodes'].items():
            print(f' {no}:{num} ', end="|")
        print()
        print("-=" * (TERMINAL_WIDTH//2))
        questionary.print("Escolha uma opção para editar os nós:", style="fg:cyan")
        escolha = questionary.select(
            "Opção:",
            choices=[
                "1. Adicionar Nó",
                "1-1. Adicionar Nó e Conectar Arestas",
                "2. Editar Nó",
                "3. Remover Nó",
                "4. Conectar Nó",
                "5. Remover Aresta",
                "6. Ver Conexões de Nó",
                self.SAIDA
                ]
        ).ask()
        return escolha
    
    def escolher_no(self, materia, assunto):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^{TERMINAL_WIDTH}}')
        print(f'{"Escolha de Nó":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        questionary.print("Escolha um nó para editar:", style="fg:cyan")
        escolha = questionary.select(
            "Nó:",
            choices= list(self.base[materia][assunto]['nodes'].keys()) + [self.SAIDA]
        ).ask()
        return escolha
    
    def adicionar_no(self, materia, assunto):
        nodes = self.base[materia][assunto]['nodes']
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))
        
        run = True
        while run:
            chave = questionary.text("Digite o nome do nó:").ask()
            if chave in nodes:
                questionary.print("Esse nó já existe. Tente novamente.", style="fg:red")
            else:
                run = False
        
        lista_valores = list(nodes.values())
        if len(lista_valores) > 0:
            assist = questionary.confirm(f"Deseja usar o número do último nó + 1? ({lista_valores[-1]} +1)", default=False).ask()
        
        if assist:
            valor = lista_valores[-1] + 1
        else:
            run = True
            while run:
                valor = questionary.text("Digite o número do nó:").ask()
                if not valor.isdigit():
                    questionary.print("O número do nó deve ser um valor inteiro. Tente novamente.", style="fg:red")
                else:
                    run = False
        nodes[chave] = int(valor)
        questionary.print(f"Nó '{chave}':{valor} adicionado com sucesso!", style="fg:green")
        input("Pressione Enter para continuar...")
        return (chave, valor)
    
    def conectar_no(self, materia, assunto, no:str):
        nodes = self.base[materia][assunto]['nodes']
        edges = self.base[materia][assunto]['edges']
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))

        # conected_nodes_as_P = []
        # conected_nodes_as_R = []
        # for edge in edges:
        #     if edge[0] == nodes[no]:
        #         conected_nodes_as_P.append(edge)
        #     if edge[1] == nodes[no]:
        #         conected_nodes_as_R.append(edge)
        
        while True:
            no_destino: str = questionary.select(
                "Escolha o outro nó:",
                choices= list(nodes.keys())
            ).ask()
            escolha = questionary.select(
                "Deseja conectar este nó como P ou R?",
                default="P",
                choices=["P", "R", self.SAIDA]
            ).ask()
            if escolha == self.SAIDA:
                questionary.print("Conexão cancelada. Voltando ao menu de edição de nós.", style="fg:cyan")
                input("Pressione Enter para continuar...")
                break
            if escolha == "P":
                # conectar como P
                edges.append([nodes[no], nodes[no_destino]])
                questionary.print(f"Nó '{no}:{nodes[no]}' conectou-se como Pergunta para '{no_destino}:{nodes[no_destino]}'", style="fg:green")
                # conected_nodes_as_P.append([nodes[no], nodes[no_destino]])
            else:
                # conectar como R
                edges.append([nodes[no_destino], nodes[no]])
                questionary.print(f"Nó '{no}:{nodes[no]}' conectou-se como Resposta para '{no_destino}:{nodes[no_destino]}'", style="fg:green")
                # conected_nodes_as_R.append([nodes[no_destino], nodes[no]])

        # questionary.print(f"Nós conectados como P: {conected_nodes_as_P}")
        # questionary.print(f"Nós conectados como R: {conected_nodes_as_R}")
    
    def full_conectar_no(self, materia, assunto, no:str):
        nodes = self.base[materia][assunto]['nodes']
        edges = self.base[materia][assunto]['edges']
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))

        escolha = questionary.select(
            "Deseja conectar este nó como P ou R?",
            default="P",
            choices=["P", "R","PR", self.SAIDA]
        ).ask()
        if escolha == self.SAIDA:
            questionary.print("Conexão cancelada. Voltando ao menu de edição de nós.", style="fg:cyan")
            input("Pressione Enter para continuar...")
            return 0
        if escolha == "PR":
            # conectar como P
            choices = []
            for node in nodes:
                add = True
                for edge in edges:
                    if edge[0] == nodes[no] and edge[1] == nodes[node]:
                        choices.append(Choice(title=f"{node}", value=edge[1], checked=True))
                        add = False
                        break
                if add:
                    choices.append(Choice(title=f"{node}", value=nodes[node], checked=False))
            no_destino: str = questionary.checkbox(
                "Escolha o outro nó:",
                choices= choices
            ).ask()
            for destino in no_destino:
                add = True
                for edge in edges:
                    if edge[0] == nodes[no] and edge[1] == destino:
                        questionary.print(f"Nó '{no}:{nodes[no]}' já conectado como Pergunta para 'X:{destino}'", style="fg:yellow")
                        add = False
                        break
                if add:
                    edges.append([nodes[no], destino])
                    questionary.print(f"Nó '{no}:{nodes[no]}' conectou-se como Pergunta para 'X:{destino}'", style="fg:green")
                add = True
                for edge in edges:
                    if edge[0] == destino and edge[1] == nodes[no]:
                        questionary.print(f"Nó '{no}:{nodes[no]}' já conectado como Resposta para 'X:{destino}'", style="fg:yellow")
                        add = False
                        break
                if add:
                    edges.append([destino, nodes[no]])
                    questionary.print(f"Nó '{no}:{nodes[no]}' conectou-se como Resposta para 'X:{destino}'", style="fg:green")
            questionary.print(f"Nós '{no}:{nodes[no]}' conectados para {no_destino}", style="fg:green")
            input()
            return 1
        elif escolha == "P":
            # conectar como P
            choices = []
            for node in nodes:
                add = True
                for edge in edges:
                    if edge[0] == nodes[no] and edge[1] == nodes[node]:
                        choices.append(Choice(title=f"{node}", value=edge[1], checked=True))
                        add = False
                        break
                if add:
                    choices.append(Choice(title=f"{node}", value=nodes[node], checked=False))
            no_destino: str = questionary.checkbox(
                "Escolha o outro nó:",
                choices= choices
            ).ask()
            for destino in no_destino:
                add = True
                for edge in edges:
                    if edge[0] == nodes[no] and edge[1] == destino:
                        questionary.print(f"Nó '{no}:{nodes[no]}' já conectado como Pergunta para 'X:{destino}'", style="fg:yellow")
                        add = False
                        break
                if add:
                    edges.append([nodes[no], destino])
                    questionary.print(f"Nó '{no}:{nodes[no]}' conectou-se como Pergunta para 'X:{destino}'", style="fg:green")
            questionary.print(f"Nós '{no}:{nodes[no]}' conectados como Pergunta para {no_destino}", style="fg:green")
            input()
            return 1
        else:
            # conectar como R
            choices = []
            for node in nodes:
                add = True
                for edge in edges:
                    if edge[0] == nodes[node] and edge[1] == nodes[no]:
                        choices.append(Choice(title=f"{node}", value=edge[1], checked=True))
                        add = False
                        break
                if add:
                    choices.append(Choice(title=f"{node}", value=nodes[node], checked=False))
            no_destino: str = questionary.checkbox(
                "Escolha o outro nó:",
                choices= choices
            ).ask()
            for destino in no_destino:
                add = True
                for edge in edges:
                    if edge[0] == destino and edge[1] == nodes[no]:
                        questionary.print(f"Nó '{no}:{nodes[no]}' já conectado como Resposta para 'X:{destino}'", style="fg:yellow")
                        add = False
                        break
                if add:
                    edges.append([destino, nodes[no]])
                    questionary.print(f"Nó '{no}:{nodes[no]}' conectou-se como Resposta para 'X:{destino}'", style="fg:green")
            questionary.print(f"Nós '{no}:{nodes[no]}' conectados como Resposta para {no_destino}", style="fg:green")
            input()
            return 1

    def editar_no(self, materia, assunto, no: str):
        nodes = self.base[materia][assunto]['nodes']
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"EDITOR DE NÓS":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f"Nó: {no}:{nodes[no]}")
        while True:
            novo_nome = questionary.text("Digite o novo nome do nó:").ask()
            if not novo_nome.strip():
                questionary.print("Nome inválido. Nenhum alteração foi feita.", style="fg:red")
                input("Pressione Enter para continuar...")
                continue
            break
        self.base[materia][assunto]['nodes'][no] = novo_nome
        questionary.print(f"Nó '{no}:{nodes[no]}' editado para '{no}:{novo_nome}'", style="fg:green")
        input("Pressione Enter para continuar...")

    def remover_no(self, materia, assunto, no: str):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'REMOVENDO NÓ "{no}"')
        escolha = questionary.confirm(f"Tem certeza que deseja remover o nó '{no}'? Isso também removerá todas as conexões associadas a ele.", default=False).ask()
        if escolha:
            # remover conexões associadas
            nodes = self.base[materia][assunto]['nodes']
            edges = self.base[materia][assunto]['edges'][:]
            no_id = nodes[no]
            for edge in edges:
                if edge[0] == no_id or edge[1] == no_id:
                    self.base[materia][assunto]['edges'].remove(edge)
            # remover nó
            del nodes[no]
            questionary.print(f"Nó '{no}' e suas conexões foram removidos com sucesso!", style="fg:green")
            input()
            return 1
        else:
            questionary.print(f'Nó {no} não removido, retornando...', style='fg:green')
        return 0

    def remover_aresta(self, materia, assunto, no: str):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))
        nodes = self.base[materia][assunto]['nodes']
        edges = self.base[materia][assunto]['edges']
        targets = []
        for edge in edges:
            if nodes[no] == edge[0] or nodes[no] == edge[1]:
                targets.append(Choice(f"[{find_key_by_value(nodes, edge[0])},{find_key_by_value(nodes, edge[1])}]", edge))
        
        to_remove = questionary.checkbox(
            f"Quais arestas do nó {no} você quer remover?",
            choices=targets
            ).ask()
        for item in to_remove:
            edges.remove(item)
            questionary.print(f"Aresta {item} removida com sucesso!", style="fg:green")
        input("Pressione Enter para continuar...")

    def ver_conexoes_no(self, materia, assunto, no: str):
        cls()
        nodes = self.base[materia][assunto]['nodes']
        edges = self.base[materia][assunto]['edges']
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"VISUALIZAÇÃO DE CONEXÕES DE NÓ":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        todos_nos = 0
        for edge in range(len(list(edges))):
            if edges[edge][0] == nodes[no]:
                print(f"Nó '{no}' conectado como Pergunta para '{find_key_by_value(nodes, edges[edge][1])}'")
                todos_nos += 1
            elif edges[edge][1] == nodes[no]:
                print(f"Nó '{no}' conectado como Resposta para '{find_key_by_value(nodes, edges[edge][0])}'")
                todos_nos += 1
        print("-=" * (TERMINAL_WIDTH//2))
        print(f"Total de conexões para o nó '{no}': {todos_nos} conexões")
        questionary.print("Pressione Enter para continuar...", style="fg:cyan")
        input()

    def exibe_nos(self, materia, assunto):
        cls()
        print(f'>/{materia}/{assunto}')
        print("-=" * (TERMINAL_WIDTH//2))
        print(f'{"EDITOR DE BASE DE PERGUNTAS":^{TERMINAL_WIDTH}}')
        print(f'{"Exibição de Nós":^{TERMINAL_WIDTH}}')
        print("-=" * (TERMINAL_WIDTH//2))
        for no, num in self.base[materia][assunto]['nodes'].items():
            print(f' {no}:{num} ', end="|")
        print()
        print("-=" * (TERMINAL_WIDTH//2))
        questionary.print("Pressione Enter para continuar...", style="fg:cyan")
        input()
    
    def run(self):
         while True:
            MP = self.menu_principal()
            match MP:
                case "1. Navegar em Matérias":
                    a_materia = self.selecionar_materia()
                    if a_materia == self.SAIDA:
                        continue
                    while True:
                        MM = self.menu_materia(a_materia)
                        match MM:
                            case "1. Navegar em Assuntos":
                                o_assunto = self.selecionar_assunto(a_materia)
                                if o_assunto == self.SAIDA:
                                    continue
                                while True:
                                    MA = self.menu_assunto(a_materia, o_assunto)
                                    match MA:
                                        case "1. Exibir Nós":
                                            self.exibe_nos(a_materia, o_assunto)
                                        case "2. Editar Nós":
                                            while True:
                                                ME = self.menu_editar_nos(a_materia, o_assunto)
                                                if ME == self.SAIDA:
                                                    break
                                                elif ME == "1. Adicionar Nó":
                                                    self.adicionar_no(a_materia, o_assunto)
                                                    continue
                                                elif ME == "1-1. Adicionar Nó e Conectar Arestas":
                                                    no, valor = self.adicionar_no(a_materia, o_assunto)
                                                    self.full_conectar_no(a_materia, o_assunto, no)
                                                    continue
                                                o_no = self.escolher_no(a_materia, o_assunto)
                                                if o_no == self.SAIDA:
                                                    break
                                                match ME:
                                                    case "2. Editar Nó":
                                                        self.editar_no(a_materia, o_assunto,o_no)
                                                    case "3. Remover Nó":
                                                        self.remover_no(a_materia, o_assunto,o_no)
                                                    case "4. Conectar Nó":
                                                        self.full_conectar_no(a_materia, o_assunto,o_no)
                                                    case "5. Remover Aresta":
                                                        self.remover_aresta(a_materia, o_assunto,o_no)
                                                    case "6. Ver Conexões de Nó":
                                                        self.ver_conexoes_no(a_materia, o_assunto,o_no)
                                        case self.SAIDA:
                                            break
                            case "2. Adicionar Assunto":
                                self.adicionar_assunto(a_materia)
                            case "3. Editar Nome de Assunto":
                                self.editar_nome_assunto(a_materia)
                            case "4. Remover Assunto":
                                self.remover_assunto(a_materia, self.selecionar_assunto(a_materia))
                            case self.SAIDA:
                                break
                case "2. Adicionar Matéria":
                    self.adicionar_materia()
                case "3. Editar Nome de Matéria":
                    self.editar_nome_materia(self.selecionar_materia())
                case "4. Remover Matéria":
                    self.remover_materia(self.selecionar_materia())
                case "0. Sair e Salvar":
                    self.save_base()
                    break


if __name__ == "__main__":
    editor = Editor()