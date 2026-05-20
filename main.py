from services.ia import perguntar_ia

def main():
    print("💳 Amon - Assistente Financeiro iniciado")
    print("Digite 'sair' para encerrar\n")

    historico = []

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() == "sair":
            print("Encerrando Amon...")
            break

        resposta = perguntar_ia(pergunta, historico)

        historico.append({"role": "user", "content": pergunta})
        historico.append({"role": "assistant", "content": resposta})

        print(f"Amon: {resposta}\n")


if __name__ == "__main__":
    main()