import os
import time
import streamlit as st
from openai import OpenAI, APIError, APITimeoutError, RateLimitError
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# Configuração
# ─────────────────────────────────────────────
load_dotenv()

# ✅ Seguro tanto local (.env) quanto em produção (st.secrets)
def _get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        try:
            key = st.secrets["OPENAI_API_KEY"]
        except (AttributeError, KeyError):
            pass
    if not key:
        raise EnvironmentError(
            "OPENAI_API_KEY não encontrada. "
            "Defina no .env (local) ou em st.secrets (produção)."
        )
    return key

client = OpenAI(
    api_key=_get_api_key(),
    base_url="https://openrouter.ai/api/v1",
    timeout=20.0,       # ✅ evita travamento silencioso
)

# ─────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────
MODELO = "meta-llama/llama-3-8b-instruct"
# 💡 Para melhor PT-BR, considere: "mistralai/mistral-7b-instruct" ou
#    "openai/gpt-4o-mini" — muito melhor em português com custo baixo.

MAX_TOKENS = 350          # um pouco mais de margem sem explodir
MAX_HISTORICO = 10        # ✅ limita janela de contexto (5 pares user/assistant)
MAX_TENTATIVAS = 2        # ✅ retry automático em falha transitória
PAUSA_RETRY = 1.5         # segundos entre tentativas

SYSTEM_PROMPT_BASE = (
    "Você é Amon, um assistente financeiro pessoal brasileiro.\n"
    "Responda SEMPRE em português do Brasil, sem exceções.\n"
    "Seja claro, objetivo e direto.\n"
    "Use frases curtas e práticas.\n"
    "Explique de forma simples, como se falasse com um amigo.\n"
    "Use no máximo 5 linhas por resposta.\n"
    "Se não souber algo, diga honestamente que não tem certeza.\n"
    "Nunca invente dados, taxas ou informações financeiras.\n"
)

# ─────────────────────────────────────────────
# Intenção
# ─────────────────────────────────────────────
_INTENCOES = {
    "investimento": (
        ["investir", "investimento", "aplicar", "rendimento", "tesouro", "ações", "fundo"],
        "Dê sugestões básicas de investimento considerando perfil conservador/baixo risco.",
    ),
    "economia": (
        ["economizar", "poupar", "cortar gastos", "gastar menos"],
        "Sugira formas práticas de economizar dinheiro no dia a dia.",
    ),
    "divida": (
        ["dívida", "divida", "devendo", "negativado", "juros", "parcelado"],
        "Ajude com estratégias para sair de dívidas, priorizando as de maior juros.",
    ),
    "renda": (
        ["salário", "renda", "ganho", "receita", "orçamento", "organizar"],
        "Explique de forma simples como organizar renda e despesas mensais.",
    ),
    "planejamento": (
        ["meta", "objetivo", "aposentadoria", "reserva", "emergência"],
        "Ajude com planejamento financeiro de curto e longo prazo.",
    ),
}

def detectar_intencao(pergunta: str) -> tuple[str, str]:
    """Retorna (nome_intencao, contexto_extra)."""
    texto = pergunta.lower()
    for nome, (palavras, contexto) in _INTENCOES.items():
        if any(p in texto for p in palavras):
            return nome, contexto
    return "geral", ""


# ─────────────────────────────────────────────
# Validação de resposta
# ─────────────────────────────────────────────

# ✅ Lista mais precisa — só sequências que NÃO ocorrem em PT-BR legítimo
_LIXO_INDICADORES = ["///", "***", "###", "```", "----", "===="]

# ✅ Bigrams que indicam inglês real (não confundem com PT-BR)
_BIGRAMS_INGLES = [
    "this is", "that is", "it is", "we are", "they are",
    "you are", "i am", "do not", "does not", "can not",
    "the best", "the most", "the only",
]

def _validar_resposta(texto: str) -> str | None:
    """
    Retorna mensagem de erro se a resposta for inválida, ou None se estiver OK.
    """
    if len(texto.split()) < 5:
        return "⚠️ Não consegui gerar uma resposta útil. Pode reformular?"

    texto_lower = texto.lower()
    if any(bi in texto_lower for bi in _BIGRAMS_INGLES):
        return "⚠️ A resposta saiu no idioma errado. Tente novamente."

    if any(s in texto for s in _LIXO_INDICADORES):
        return "⚠️ Ocorreu um erro na formatação da resposta. Tente novamente."

    return None  # ✅ resposta OK


# ─────────────────────────────────────────────
# Função principal
# ─────────────────────────────────────────────

def perguntar_ia(pergunta: str, historico: list[dict]) -> str:
    """
    Envia a pergunta para o modelo e retorna a resposta formatada.

    Args:
        pergunta:  texto do usuário
        historico: lista de dicts {"role": ..., "content": ...}
                   (apenas mensagens anteriores, SEM a pergunta atual)

    Returns:
        String com a resposta do Amon (ou mensagem de erro amigável).
    """
    intencao, contexto_extra = detectar_intencao(pergunta)

    # ✅ Monta system prompt dinâmico de forma limpa
    system_content = SYSTEM_PROMPT_BASE
    if contexto_extra:
        system_content += f"\nContexto desta conversa: {contexto_extra}"

    # ✅ Limita histórico para não explodir o contexto
    historico_limitado = historico[-(MAX_HISTORICO):]

    messages = (
        [{"role": "system", "content": system_content}]
        + historico_limitado
        + [{"role": "user", "content": pergunta}]
    )

    ultimo_erro: Exception | None = None

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            resposta = client.chat.completions.create(
                model=MODELO,
                max_tokens=MAX_TOKENS,
                temperature=0.4,   # ✅ mais consistente para finanças
                messages=messages,
            )

            texto = resposta.choices[0].message.content.strip()

            # ✅ Valida qualidade
            erro_validacao = _validar_resposta(texto)
            if erro_validacao:
                # Na última tentativa, entrega o erro; senão tenta de novo
                if tentativa == MAX_TENTATIVAS:
                    return erro_validacao
                time.sleep(PAUSA_RETRY)
                continue

            # ✅ Trunca se necessário (sem cortar no meio de uma palavra)
            if len(texto) > 800:
                texto = texto[:797].rsplit(" ", 1)[0] + "…"

            return f"💡 {texto}"

        except RateLimitError:
            return "⚠️ Muitas requisições. Aguarde alguns segundos e tente novamente."

        except APITimeoutError:
            ultimo_erro = APITimeoutError("timeout")
            if tentativa < MAX_TENTATIVAS:
                time.sleep(PAUSA_RETRY)

        except APIError as e:
            ultimo_erro = e
            if tentativa < MAX_TENTATIVAS:
                time.sleep(PAUSA_RETRY)

        except Exception as e:
            # Erros inesperados — não faz retry
            # Em produção, logue aqui: logging.exception(e)
            return "⚠️ O Amon encontrou um erro inesperado. Tente novamente em instantes."

    # Esgotou as tentativas
    return "⚠️ O serviço está instável no momento. Tente novamente em breve."