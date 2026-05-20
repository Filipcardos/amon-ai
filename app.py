import streamlit as st
from services.ia import perguntar_ia
import time

st.set_page_config(page_title="Amon AI", layout="centered")

# 🎨 CSS COMPLETO (visual + animações)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #0d1117, #02040a);
    color: white;
}

/* Centralização */
.chat-container {
    max-width: 700px;
    margin: auto;
    padding-top: 30px;
}

/* Mensagens */
.user-msg {
    background-color: #1f2937;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    text-align: right;
}

.bot-msg {
    background-color: #111827;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 3px solid #00c896;
}

/* Fade animation */
.bot-msg, .user-msg {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Hover leve */
.bot-msg:hover, .user-msg:hover {
    transform: scale(1.01);
    transition: 0.2s;
}

/* Avatar */
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}

/* Header */
.title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #999;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ✅ Header estilo app real
st.markdown('<div class="title">🤖 Amon AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Como posso te ajudar com suas finanças hoje?</div>', unsafe_allow_html=True)

# ✅ Histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# ✅ Função efeito digitando
def efeito_digitando(texto):
    placeholder = st.empty()
    texto_parcial = ""

    for char in texto:
        texto_parcial += char
        placeholder.markdown(f'<div class="bot-msg">💡 {texto_parcial}</div>', unsafe_allow_html=True)
        time.sleep(0.01)

# ✅ Render chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.historico:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end;">
            <div class="user-msg">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; gap: 8px;">
            <img class="avatar" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png">
            <div class="bot-msg">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ✅ Input estilo chat
pergunta = st.chat_input("Digite sua pergunta...")

# ✅ Processamento
if pergunta:

    # salva usuário
    st.session_state.historico.append({"role": "user", "content": pergunta})

    # simulação simples
    if "juros" in pergunta.lower():
        resposta = "📊 Para simular juros com precisão, utilize um cálculo detalhado (versão futura interativa)."

        st.session_state.historico.append({"role": "assistant", "content": resposta})
        st.rerun()

    with st.spinner("🤖 Amon está pensando..."):
        resposta = perguntar_ia(pergunta, st.session_state.historico)

    st.session_state.historico.append({"role": "assistant", "content": resposta})

    st.rerun()