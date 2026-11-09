# Amon AI — Assistente de educação financeira

Assistente de educação financeira em Python, Streamlit e OpenRouter, desenvolvido por Filipe Oliveira Cardoso.

## Recursos

- Chat em português brasileiro com histórico contextual, sem duplicação da última pergunta.
- Interface com componentes nativos do Streamlit.
- Modelo do OpenRouter configurável (padrão: `openrouter/free`).
- Tratamento de falhas de autenticação, conexão, limites e respostas vazias.
- Simulador determinístico de juros compostos com aportes mensais e gráfico.
- Exportação do histórico em JSON e opção para iniciar uma nova conversa.
- Testes automatizados e pipeline de CI no GitHub Actions.

## Instalação

Requer Python 3.10 ou superior.

1. Clone o repositório.
2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Copie `.env.example` para `.env` e informe uma chave do [OpenRouter](https://openrouter.ai/keys):

```env
OPENROUTER_API_KEY=sua_chave_aqui
OPENROUTER_MODEL=openrouter/free
```

4. Inicie o aplicativo:

```bash
streamlit run app.py
```

Opcionalmente, execute o chat no terminal com `python main.py`.

### Streamlit Community Cloud

Em **Settings > Secrets**, defina `OPENROUTER_API_KEY` com sua chave e, opcionalmente, `OPENROUTER_MODEL`. Nunca envie chaves reais ao repositório.

## Testes

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

Os testes unitários simulam as chamadas à API e não exigem acesso à internet.

## Limitações

- O roteador `openrouter/free` pode variar de modelo e tem restrições de uso.
- O histórico fica somente na sessão atual; exporte-o em JSON caso precise salvá-lo.
- O Amon não acessa saldos bancários, cotações ou notícias em tempo real.
- A simulação de juros usa taxa mensal hipotética e aporte ao final de cada mês, sem tributos, inflação ou tarifas.
- Informações fornecidas são educativas e não constituem recomendação financeira individualizada.
- Evite enviar dados bancários sensíveis ou confidenciais ao serviço de IA.

## Estrutura

- `app.py`: interface Streamlit.
- `main.py`: chat opcional no terminal.
- `services/ia.py`: montagem do contexto e conexão com OpenRouter.
- `services/calculos.py`: simulador de juros.
- `tests/`: testes automatizados.
- `.github/workflows/ci.yml`: validação no GitHub Actions.

**Projeto:** [Filipcardos/amon-ai](https://github.com/Filipcardos/amon-ai)
