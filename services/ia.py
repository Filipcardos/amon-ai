import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def perguntar_ia(pergunta, historico):
    try:
        resposta = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é Amon, um assistente financeiro inteligente e confiável. "
                        "Responda de forma clara, objetiva e profissional. "
                        "Ajude com finanças pessoais, investimentos, orçamento e dúvidas financeiras. "
                        "Se não souber, diga que não sabe e sugira alternativas. "
                        "Nunca invente informações."
                    )
                }
            ] + historico + [
                {"role": "user", "content": pergunta}
            ]
        )

        resposta_texto = resposta.choices[0].message.content.strip()

        if "não sei" in resposta_texto.lower():
            resposta_texto += "\n\n👉 Sugestão: reformule a pergunta ou consulte fontes confiáveis."

        return resposta_texto

    except Exception as e:
        return f"⚠️ Erro ao consultar Amon: {str(e)}"
