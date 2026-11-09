<div align="center">

<img width="100%" alt="Banner do Amon AI" src="https://github.com/user-attachments/assets/edab3b1e-6dd7-4535-9207-9e7df90dc07e" />

# Amon AI
### Assistente financeiro com inteligência artificial

**Um assistente conversacional para tornar a educação financeira mais acessível, clara e prática.**

[**Experimentar aplicação**](https://amon-ai.streamlit.app/) · [**Ver código-fonte**](https://github.com/Filipcardos/amon-ai) · [**Melhorias em desenvolvimento**](https://github.com/Filipcardos/amon-ai/pull/1)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?logo=streamlit&logoColor=white)
![OpenRouter](https://img.shields.io/badge/IA-OpenRouter-5636C3)
![Licença](https://img.shields.io/github/license/Filipcardos/amon-ai)

</div>

---

## Sobre o projeto

O **Amon AI** é um assistente virtual desenvolvido em **Python** com interface em **Streamlit** e integração a modelos de linguagem por meio do **OpenRouter** (usando o SDK da OpenAI).

Seu objetivo é responder perguntas sobre finanças pessoais em linguagem natural, com foco em **organização do orçamento, economia, dívidas, investimentos e planejamento financeiro**.

O projeto nasceu de um desafio da **DIO** e foi desenvolvido como prática de integração com APIs, inteligência artificial generativa, desenvolvimento web e experiência do usuário.

> **Aviso:** o Amon oferece conteúdo educativo. As respostas não constituem consultoria financeira individualizada ou garantia de resultados.

## Acesse a aplicação

**[Abrir o Amon AI no Streamlit](https://amon-ai.streamlit.app/)**

Você pode testar perguntas como:

- "Como organizar meu salário e minhas despesas mensais?"
- "Qual a diferença entre reserva de emergência e investimento?"
- "Quais passos ajudam a sair das dívidas?"
- "Como começar a investir com pouco dinheiro?"

*A disponibilidade da aplicação e dos modelos depende do serviço de hospedagem e da API configurada.*

## Funcionalidades da versão principal

| Funcionalidade | Descrição |
|---|---|
| Chat com IA | Perguntas e respostas sobre finanças pessoais em português brasileiro |
| Histórico em sessão | Mantém mensagens durante o uso da sessão atual |
| Identificação de intenção | Categoriza perguntas sobre investimentos, economia, dívidas, renda e planejamento |
| Respostas contextualizadas | Utiliza instruções e mensagens anteriores para orientar as respostas |
| Interface Streamlit | Layout escuro com apresentação em formato de conversa |
| Integração OpenRouter | Envia solicitações a um modelo de linguagem usando API compatível com OpenAI |
| Tratamento de falhas | Aplica tentativas em alguns erros transitórios e retorna mensagens amigáveis |

### Em evolução

Há uma atualização proposta no **[Pull Request #1](https://github.com/Filipcardos/amon-ai/pull/1)**, que inclui correções do histórico, chat com componentes nativos do Streamlit, modelo configurável, simulador de juros compostos, exportação de conversas e testes automatizados.

**Esses recursos ainda não estão disponíveis na branch `main` até a integração do Pull Request.**

## Tecnologias

- **Python:** lógica da aplicação e integração entre componentes.
- **Streamlit:** interface web interativa.
- **OpenRouter:** acesso a modelos de IA.
- **OpenAI SDK:** cliente Python compatível com o endpoint do OpenRouter.
- **python-dotenv:** carregamento de variáveis de ambiente no desenvolvimento local.
- **Git e GitHub:** versionamento do código e publicação.

## Arquitetura

```text
amon-ai/
├── app.py              # Interface web com Streamlit
├── main.py             # Interação opcional via terminal
├── services/
│   └── ia.py           # Integração com o modelo e regras do assistente
├── requirements.txt    # Dependências Python
├── .gitignore
└── README.md
```

**Fluxo simplificado:**

```text
Usuário → Streamlit → services/ia.py → OpenRouter → Modelo de IA
                                              ↓
Usuário ← Resposta na interface ← Resposta processada
```

## Como executar localmente

### 1. Pré-requisitos

- Python **3.10 ou superior**.
- Git (opcional, caso baixe o projeto como ZIP).
- Uma chave de API válida do [OpenRouter](https://openrouter.ai/keys).

### 2. Clone o repositório

```bash
git clone https://github.com/Filipcardos/amon-ai.git
cd amon-ai
```

### 3. Crie e ative um ambiente virtual

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Configure sua chave do OpenRouter

Na raiz do projeto, crie o arquivo **`.env`**:

```env
OPENROUTER_API_KEY=sua_chave_do_openrouter_aqui
OPENROUTER_MODEL=openrouter/free
```

A chave antiga `OPENAI_API_KEY` continua aceita para compatibilidade. O roteador `openrouter/free` seleciona um modelo gratuito disponível; consulte os [limites de uso do OpenRouter](https://openrouter.ai/collections/free-models/). Caso queira definir outro, altere `OPENROUTER_MODEL`.

### 6. Inicie a aplicação

```bash
streamlit run app.py
```

O Streamlit exibirá um endereço local (normalmente `http://localhost:8501`) para abrir no navegador.

**Alternativa:** execute `python main.py` para usar o assistente pelo terminal.

## Deploy no Streamlit Community Cloud

Para publicar no [Streamlit Community Cloud](https://share.streamlit.io/):

1. Conecte o repositório do GitHub.
2. Selecione o arquivo principal **`app.py`**.
3. Nas configurações do aplicativo, abra **Settings → Secrets**.
4. Adicione a chave no formato TOML:

```toml
OPENROUTER_API_KEY = "sua_chave_do_openrouter_aqui"
OPENROUTER_MODEL = "openrouter/free"
```

5. Salve e reinicie o aplicativo, se necessário.

**Não publique credenciais no GitHub**, no README ou em arquivos versionados.

## Segurança e limitações

- Nunca compartilhe números completos de cartões, senhas, tokens ou dados bancários confidenciais com o chat.
- O histórico da versão principal é mantido em memória de sessão, **não em banco de dados**.
- O assistente não consulta automaticamente seu saldo, dados bancários ou cotações em tempo real.
- Respostas geradas por IA podem conter erros: valide números, taxas e orientações antes de tomar decisões.
- A configuração de cada modelo e a disponibilidade da API podem mudar conforme o provedor.

## Evolução do projeto

O Amon AI está em aprimoramento contínuo. Entre os objetivos estão maior confiabilidade do contexto conversacional, simulações matemáticas independentes do modelo de linguagem, testes automatizados e uma base para futuras integrações com dados e dashboards.

Acompanhe as alterações em [Pull Requests](https://github.com/Filipcardos/amon-ai/pulls).

## Autor

**Filipe Oliveira Cardoso**

Bacharel em Administração e estudante de Análise e Desenvolvimento de Sistemas. Interesse em desenvolvimento Python, IA, dados, automação e soluções que conectem tecnologia a problemas reais.

[LinkedIn](https://www.linkedin.com/in/filipe-cardoso-919532205/) · [Portfólio](https://filipe-cardoso.vercel.app/) · [GitHub](https://github.com/Filipcardos)

---

<div align="center">

Desenvolvido com **Python, Streamlit e inteligência artificial**.

Se o projeto foi útil, considere deixar uma ⭐ no repositório.

</div>
