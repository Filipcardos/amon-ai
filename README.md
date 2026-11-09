<div align="center">

<img width="100%" alt="Banner do Amon AI" src="https://github.com/user-attachments/assets/edab3b1e-6dd7-4535-9207-9e7df90dc07e" />

# Amon AI
### Assistente financeiro com inteligência artificial

**Um assistente conversacional para tornar a educação financeira mais acessível, clara e prática.**

[**Experimentar aplicação**](https://amon-ai.streamlit.app/) · [**Ver código-fonte**](https://github.com/Filipcardos/amon-ai) · [**Ver atualização proposta**](https://github.com/Filipcardos/amon-ai/pull/1)

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

## Funcionalidades da versão aprimorada

| Funcionalidade | Descrição |
|---|---|
| Chat com IA | Conversa em português brasileiro com histórico contextual sem duplicar a pergunta |
| Histórico e exportação | Mantém mensagens na sessão, permite limpar e exportar o histórico em JSON |
| Integração OpenRouter | Modelo configurável na barra lateral (padrão: `openrouter/free`) |
| Simulador financeiro | Juros compostos com capital inicial, aportes mensais, taxa e prazo |
| Visualização | Gráfico de evolução do saldo e métricas em reais |
| Interface Streamlit | Componentes nativos de chat e controles interativos |
| Tratamento de erros | Mensagens específicas para chave inválida, limite, conexão e respostas vazias |
| Testes automatizados | Testes com cliente da API simulado e workflow GitHub Actions |

### Próximos passos

Persistência opcional das conversas, melhorias de acessibilidade, cenários financeiros adicionais e integração segura com dados fornecidos pelo próprio usuário.

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
│   ├── ia.py           # Integração com OpenRouter
│   └── calculos.py     # Cálculos de juros compostos
├── tests/               # Testes unitários
├── .github/workflows/
│   └── ci.yml           # Automação de testes
├── .env.example         # Modelo de variáveis de ambiente
├── requirements.txt
├── requirements-dev.txt
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
- Uma chave de API válida do [OpenRouter](https://openrouter.ai/keys). O roteador gratuito pode ter limites de uso.

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

Copie `.env.example` para `.env` e preencha sua chave:

```env
OPENROUTER_API_KEY=sua_chave_do_openrouter_aqui
OPENROUTER_MODEL=openrouter/free
```

É possível trocar o modelo também pela barra lateral da aplicação. Verifique se o ID escolhido está disponível em sua conta do OpenRouter.

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

## Testes automatizados

Os testes cobrem montagem de contexto, prevenção de pergunta duplicada, resposta da IA simulada, validação de entrada e simulações matemáticas.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Os testes unitários não exigem uma chave real do OpenRouter. A execução integrada da interface e uma chamada real à API devem ser verificadas separadamente.

## Segurança e limitações

- Nunca compartilhe números completos de cartões, senhas, tokens ou dados bancários confidenciais com o chat.
- O histórico é mantido na sessão atual, **não em banco de dados**. Você pode exportá-lo em JSON.
- O assistente não consulta automaticamente seu saldo, dados bancários ou cotações em tempo real.
- O simulador utiliza juros compostos com aporte no fim de cada mês e não considera taxas, tributos nem inflação.
- Respostas geradas por IA podem conter erros: valide números, taxas e orientações antes de tomar decisões.
- A configuração de cada modelo e a disponibilidade da API podem mudar conforme o provedor.

## Evolução do projeto

O Amon AI está em aprimoramento contínuo. Esta versão introduz melhorias no contexto conversacional, simulações matemáticas independentes da IA e testes automatizados. As próximas etapas poderão incluir memória persistente, visualizações financeiras adicionais e novas integrações.

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
