"""Interface web do Amon AI."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from PIL import Image

import streamlit as st

from services.calculos import simular_juros_compostos
from services.ia import DEFAULT_MODEL, IAServiceError, perguntar_ia

LOGO_PATH = Path(__file__).resolve().parent / "assets" / "amon-logo.png"
st.set_page_config(
    page_title="Amon AI | Finanças pessoais",
    page_icon=Image.open(LOGO_PATH),
    layout="centered",
)


def configuracao(nome: str) -> str:
    """Busca configuração primeiro no ambiente, depois no Streamlit Secrets."""
    valor = os.getenv(nome)
    if valor:
        return valor
    try:
        return str(st.secrets.get(nome, ""))
    except Exception:  # st.secrets pode não estar configurado no ambiente local
        return ""


def em_reais(valor) -> str:
    return f"R$ {valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


st.markdown(
    """<style>
    .stApp {background: linear-gradient(160deg, #101722, #070b12);}
    [data-testid="stChatMessage"] {border: 1px solid #253346; border-radius: 14px;}
    [data-testid="stSidebar"] {background: #0e1520;}
    </style>""",
    unsafe_allow_html=True,  # HTML apenas ESTÁTICO, nenhum texto de usuário/IA aqui.
)

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

with st.sidebar:
    st.header("Configurações")
    modelo = st.text_input(
        "Modelo do OpenRouter",
        value=configuracao("OPENROUTER_MODEL") or DEFAULT_MODEL,
        help="openrouter/free é gratuito, mas pode variar de modelo e sofrer limites.",
    ).strip()
    api_key = configuracao("OPENROUTER_API_KEY") or configuracao("OPENAI_API_KEY")
    if not api_key:
        api_key = st.text_input(
            "Chave do OpenRouter",
            type="password",
            help="Usada apenas nesta sessão. Para produção, configure em Secrets.",
        ).strip()

    if st.button("Nova conversa", use_container_width=True):
        st.session_state.mensagens = []
        st.rerun()

    if st.session_state.mensagens:
        exportacao = {
            "aplicacao": "Amon AI",
            "exportado_em": datetime.now().astimezone().isoformat(),
            "mensagens": st.session_state.mensagens,
        }
        st.download_button(
            "Exportar conversa (JSON)",
            data=json.dumps(exportacao, ensure_ascii=False, indent=2),
            file_name="amon-conversa.json",
            mime="application/json",
            use_container_width=True,
        )
    st.caption("Seu histórico fica na sessão atual e não é armazenado em banco de dados.")
    st.caption("Não informe senhas, números de cartão ou dados bancários sensíveis no chat.")

logo_col, titulo_col = st.columns([1, 10], gap="small", vertical_alignment="center")
with logo_col:
    st.image(str(LOGO_PATH), use_container_width=True)
with titulo_col:
    st.title("Amon AI")
st.caption("Seu assistente de educação financeira, com respostas práticas em português.")

chat_tab, simulador_tab = st.tabs(["Chat com IA", "Simulador de juros"])

with chat_tab:
    for mensagem in st.session_state.mensagens:
        with st.chat_message(mensagem["role"]):
            if mensagem.get("is_error"):
                st.error(mensagem["content"])
            else:
                st.markdown(mensagem["content"])  # HTML inseguro NÃO habilitado.

    if not api_key:
        st.info("Configure sua chave do OpenRouter na barra lateral para começar.")

    pergunta = st.chat_input(
        "Ex.: Como montar minha reserva de emergência?",
        max_chars=2000,
        disabled=not bool(api_key) or not bool(modelo),
    )
    if pergunta:
        # Primeiro registra a pergunta para a interface. Ao modelo, envia apenas
        # o histórico ANTERIOR ([:-1]), evitando duplicação.
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)
        with st.chat_message("assistant"):
            with st.spinner("Amon está pensando..."):
                try:
                    resposta = perguntar_ia(
                        pergunta,
                        st.session_state.mensagens[:-1],
                        api_key=api_key,
                        modelo=modelo,
                    )
                    st.markdown(resposta)
                    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
                except (IAServiceError, ValueError) as erro:
                    mensagem_erro = str(erro)
                    st.error(mensagem_erro)
                    st.session_state.mensagens.append(
                        {"role": "assistant", "content": mensagem_erro, "is_error": True}
                    )

with simulador_tab:
    st.subheader("Juros compostos com aportes mensais")
    st.caption("Simulação hipotética. Aportes realizados no final de cada mês.")
    col1, col2 = st.columns(2)
    with col1:
        capital = st.number_input("Capital inicial (R$)", min_value=0.0, value=1000.0, step=100.0)
        aporte = st.number_input("Aporte mensal (R$)", min_value=0.0, value=200.0, step=50.0)
    with col2:
        taxa = st.number_input("Taxa mensal hipotética (%)", min_value=-100.0, max_value=100.0, value=0.70, step=0.1)
        meses = st.number_input("Prazo (meses)", min_value=1, max_value=600, value=24, step=1)

    resultado = simular_juros_compostos(capital, aporte, taxa, int(meses))
    c1, c2, c3 = st.columns(3)
    c1.metric("Saldo final", em_reais(resultado["valor_final"]))
    c2.metric("Total aplicado", em_reais(resultado["total_investido"]))
    c3.metric("Rendimento", em_reais(resultado["rendimento"]))
    st.line_chart({"Saldo projetado (R$)": [p["Saldo"] for p in resultado["evolucao"]]})
    st.caption("Não considera tributos, taxas, inflação ou oscilações reais. Não é promessa de rendimento.")
