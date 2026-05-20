
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# ✅ Carregar variáveis locais
load_dotenv()

# ✅ Pegar chave (local ou produção)
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# ✅ Cliente OpenRouter
client = OpenAI(
    api_key=api_key,
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
                        "Você é Amon, um assistente financeiro digital brasileiro.\n"
                        "Responda SEMPRE em português do Brasil.\n"
                        "Seja claro, objetivo e profissional.\n"
                        "Explique conceitos financeiros de forma simples.\n"
                        "Responda em no máximo 5 linhas.\n"
                        "Use exemplos práticos quando possível.\n"
                        "Evite respostas genéricas.\n"
                        "Se não souber a resposta, diga que não tem certeza e sugira caminhos confiáveis.\n"
                        "Nunca invente informações.\n"
                    )
                }
            ] + historico + [
                {"role": "user", "content": pergunta}
            ]
        )

        resposta_texto = resposta.choices[0].message.content.strip()

        # ✅ Filtro de idioma (caso saia em inglês)
        palavras_ingles = ["the ", "is ", "are ", "this ", "that ", "with ", "from "]

        if any(p in resposta_texto.lower() for p in palavras_ingles):
            return "⚠️ Tive dificuldade em responder corretamente. Pode reformular sua pergunta?"

        # ✅ Limitar respostas muito grandes
        if len(resposta_texto) > 800:
            resposta_texto = resposta_texto[:800] + "..."

        # ✅ Padronizar resposta
        resposta_texto = f"💡 {resposta_texto}"

        return resposta_texto

    except Exception as e:
        return "⚠️ O Amon encontrou um erro ao responder. Tente novamente em instantes."
