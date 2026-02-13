from editor import Editor, cls, TERMINAL_WIDTH
from perguntas import Perguntas

editor = Editor()
perguntas = Perguntas()

def main():
    while True:
        cls()
        print("\n" + "=" * TERMINAL_WIDTH)
        print(f'{"Menu Principal":^{TERMINAL_WIDTH}}')
        print("=" * TERMINAL_WIDTH)
        print("1. Editor")
        print("2. Jogo de Perguntas")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        match opcao:
            case "1":
                editor.run()
            case "2":
                perguntas.new_run()
            case "3":
                print("Até logo!")
                break
            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()