"""Modo opcional do Amon pelo terminal: python main.py."""

from services.ia import IAServiceError, perguntar_ia


def main() -> None:
    print("Amon AI — educação financeira. Digite 'sair' para encerrar.\n")
    historico: list[dict] = []
    while True:
        try:
            pergunta = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando Amon.")
            break
        if pergunta.lower() == "sair":
            break
        if not pergunta:
            continue
        try:
            resposta = perguntar_ia(pergunta, historico)
        except (IAServiceError, ValueError) as erro:
            print(f"Amon: {erro}\n")
            continue
        historico.extend([
            {"role": "user", "content": pergunta},
            {"role": "assistant", "content": resposta},
        ])
        print(f"Amon: {resposta}\n")


if __name__ == "__main__":
    main()
