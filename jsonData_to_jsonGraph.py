import json

def flatten_text(item):
    """Converte item em lista de strings (total flatten)."""
    if isinstance(item, str):
        return [item]
    if isinstance(item, list):
        result = []
        for x in item:
            if isinstance(x, list):
                result.extend(flatten_text(x))
            else:
                result.append(x)
        return result
    return []

def menu_relacao(p, r):
    """Menu para decidir a relação entre p e r."""
    print("\n-------------------------------------")
    print(f"P (pergunta): {p}")
    print(f"R (resposta): {r}")
    print("Escolha:")
    print("1 - P → R")
    print("2 - R → P")
    print("3 - P ↔ R (bidirecional)")
    print("4 - Pular (não criar relação)")

    while True:
        escolha = input("Opção (1/2/3/4): ").strip()
        if escolha in {"1", "2", "3", "4"}:
            return escolha
        print("Opção inválida, tente novamente.")

def process_subarea(lista_questoes):
    """Converte subárea para grafo com escolha individual por par P-R."""
    nodes = {}
    edges = []
    next_id = 1

    def get_id(texto):
        nonlocal next_id
        if texto not in nodes:
            nodes[texto] = next_id
            next_id += 1
        return nodes[texto]

    for item in lista_questoes:
        if len(item) != 2:
            continue

        perguntas = flatten_text(item[0])
        respostas = flatten_text(item[1])

        print("\n=====================================")
        print("Nova questão encontrada!")
        print("Perguntas:", perguntas)
        print("Respostas:", respostas)
        print("=====================================\n")

        for p in perguntas:
            id_p = get_id(p)

            for r in respostas:
                id_r = get_id(r)

                escolha = menu_relacao(p, r)

                if escolha == "1":      # P → R
                    edges.append([id_p, id_r])

                elif escolha == "2":    # R → P
                    edges.append([id_r, id_p])

                elif escolha == "3":    # P ↔ R
                    edges.append([id_p, id_r])
                    edges.append([id_r, id_p])

                elif escolha == "4":    # Pular
                    print("✓ Par ignorado.")

    return {"nodes": nodes, "edges": edges}

def converter_base_interativo(caminho="base.json", saida="base_grafo.json"):
    with open(caminho, encoding="utf-8") as f:
        base = json.load(f)

    nova_base = {}

    print("\n=== Conversão Interativa Iniciada ===\n")

    for area, subareas in base.items():
        print(f"\n##### ÁREA: {area} #####\n")
        nova_base[area] = {}

        for sub, lista_questoes in subareas.items():
            print(f"\n--- Subárea: {sub} ---")
            nova_base[area][sub] = process_subarea(lista_questoes)

    with open(saida, "w", encoding="utf-8") as f:
        json.dump(nova_base, f, ensure_ascii=False, indent=4)

    print("\n✔ Conversão concluída!")
    print(f"Arquivo gerado: {saida}")

if __name__ == "__main__":
    converter_base_interativo()
