"""Integração do Amon com modelos via OpenRouter (API compatível com OpenAI)."""

from __future__ import annotations

import logging
import os
from typing import Any

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    OpenAI,
    RateLimitError,
)

load_dotenv()
logger = logging.getLogger(__name__)

DEFAULT_MODEL = "openrouter/free"
OPENROUTER_URL = "https://openrouter.ai/api/v1"
MAX_HISTORICO = 12
MAX_PERGUNTA = 4000
MAX_RESPOSTA_TOKENS = 900

SYSTEM_PROMPT = """Você é Amon, um assistente de educação financeira para pessoas no Brasil.
Responda em português brasileiro, de maneira clara, correta, respeitosa e prática.
Ajude com orçamento, dívidas, poupança, investimentos e conceitos financeiros.
Não invente taxas, preços, notícias, regras tributárias ou dados atualizados.
Você não tem acesso automático a cotações, saldos bancários ou à internet.
Para cálculos, declare os valores, a unidade da taxa, o prazo e as hipóteses.
Se faltarem dados essenciais para um cálculo, peça-os. Não confunda taxa mensal e anual.
Em investimentos, apresente riscos e alternativas sem garantir resultados.
Não trate informações educacionais como aconselhamento financeiro individualizado.
Use listas e exemplos quando ajudarem; não corte artificialmente explicações necessárias.
"""


class IAServiceError(Exception):
    """Erro amigável e seguro para exibir na interface."""


def montar_mensagens(pergunta: str, historico: list[dict] | None = None) -> list[dict]:
    """Cria payload com a pergunta atual exatamente uma vez.

    Aceita histórico com mensagens já exibidas; se o chamador incluiu a
    pergunta atual como último item, remove a duplicata automaticamente.
    """
    pergunta = pergunta.strip()
    if not pergunta:
        raise ValueError("Digite uma pergunta para o Amon.")
    if len(pergunta) > MAX_PERGUNTA:
        raise ValueError(f"A pergunta pode ter no máximo {MAX_PERGUNTA} caracteres.")

    mensagens_anteriores: list[dict[str, str]] = []
    for msg in historico or []:
        if not isinstance(msg, dict):
            continue
        if msg.get("is_error"):
            # Um par pergunta/erro não representa uma resposta útil do modelo.
            if (msg.get("role") == "assistant" and mensagens_anteriores
                    and mensagens_anteriores[-1]["role"] == "user"):
                mensagens_anteriores.pop()
            continue
        role = msg.get("role")
        conteudo = msg.get("content")
        if role in {"user", "assistant"} and isinstance(conteudo, str) and conteudo.strip():
            mensagens_anteriores.append({"role": role, "content": conteudo[:MAX_PERGUNTA]})

    if (mensagens_anteriores and mensagens_anteriores[-1]["role"] == "user"
            and mensagens_anteriores[-1]["content"].strip() == pergunta):
        mensagens_anteriores.pop()

    mensagens_anteriores = mensagens_anteriores[-MAX_HISTORICO:]
    return (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + mensagens_anteriores
        + [{"role": "user", "content": pergunta}]
    )


def perguntar_ia(
    pergunta: str,
    historico: list[dict] | None = None,
    *,
    api_key: str | None = None,
    modelo: str | None = None,
    cliente: Any | None = None,
) -> str:
    """Consulta a IA; não altera o histórico recebido.

    api_key e modelo são opcionais para manter compatibilidade com main.py.
    O parâmetro cliente permite testes sem chamadas externas.
    """
    messages = montar_mensagens(pergunta, historico)
    modelo = (modelo or os.getenv("OPENROUTER_MODEL") or DEFAULT_MODEL).strip()

    if cliente is None:
        chave = api_key or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not chave:
            raise IAServiceError(
                "Chave do OpenRouter não configurada. Adicione OPENROUTER_API_KEY "
                "no .env ou nos Secrets do Streamlit."
            )
        cliente = OpenAI(
            api_key=chave,
            base_url=OPENROUTER_URL,
            timeout=45.0,
            max_retries=1,
        )

    try:
        resposta = cliente.chat.completions.create(
            model=modelo,
            messages=messages,
            temperature=0.3,
            max_tokens=MAX_RESPOSTA_TOKENS,
        )
        choices = getattr(resposta, "choices", None)
        if not choices:
            raise IAServiceError("O modelo não retornou uma resposta. Tente novamente.")
        conteudo = getattr(choices[0].message, "content", None)
        if not isinstance(conteudo, str) or not conteudo.strip():
            raise IAServiceError(
                "O modelo retornou uma mensagem vazia. Tente novamente ou escolha outro modelo."
            )
        return conteudo.strip()

    except AuthenticationError as exc:
        logger.warning("Falha de autenticação no OpenRouter: %s", type(exc).__name__)
        raise IAServiceError("Chave de API inválida ou sem permissão. Confira o OpenRouter.") from exc
    except RateLimitError as exc:
        raise IAServiceError("Limite de requisições atingido. Tente mais tarde ou troque o modelo.") from exc
    except (APITimeoutError, APIConnectionError) as exc:
        logger.warning("Falha de conexão com OpenRouter: %s", type(exc).__name__)
        raise IAServiceError("Não foi possível conectar ao serviço de IA. Tente novamente.") from exc
    except BadRequestError as exc:
        logger.warning("Requisição inválida ao OpenRouter: %s", type(exc).__name__)
        raise IAServiceError("O modelo escolhido não aceitou a solicitação. Confira o ID do modelo.") from exc
    except APIStatusError as exc:
        logger.warning("OpenRouter retornou HTTP %s", exc.status_code)
        raise IAServiceError("O provedor de IA está indisponível. Tente novamente mais tarde.") from exc
    except APIError as exc:
        logger.exception("Falha inesperada do SDK OpenAI/OpenRouter")
        raise IAServiceError("Houve uma falha na geração da resposta. Tente novamente.") from exc
