# WhatsApp Anamnese Bot

Chatbot de WhatsApp que conduz uma anamnese clínica geral com o paciente,
seção por seção, e gera um relatório `.docx` estruturado ao final.

## Como funciona

1. O paciente conversa com o bot pelo WhatsApp.
2. Um agente LLM conduz a anamnese seguindo um roteiro de 9 seções, fazendo
   uma pergunta por vez.
3. Um RAG sobre PDFs de protocolos clínicos enriquece as perguntas do agente.
4. Ao concluir todas as seções, um relatório `.docx` organizado é gerado na
   pasta `output/`.

```
WhatsApp -> Evolution API -> POST /webhook (FastAPI) -> agente -> resposta -> WhatsApp
```

## Stack

- **Python 3.12** — LangChain não é compatível com o Python 3.14
- **FastAPI** — webhook que recebe as mensagens
- **Evolution API** (Docker) — integração com o WhatsApp
- **LangChain + Claude** (Anthropic, Haiku 4.5) — agente conversacional
- **ChromaDB + HuggingFace embeddings** — RAG sobre os protocolos clínicos
- **python-docx** — geração do relatório final

## Pré-requisitos

- Python 3.12
- Docker e Docker Compose

## 1. Instalação

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Variáveis de ambiente

Copie `.env.example` para `.env` e preencha:

```
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=minha_chave_123
EVOLUTION_INSTANCE=anamnese-bot
ANTHROPIC_API_KEY=sua_chave_aqui
APP_ENV=development
```

- `EVOLUTION_API_KEY` deve ser igual ao `AUTHENTICATION_API_KEY` definido no
  `docker-compose.yml`.
- `ANTHROPIC_API_KEY` é a chave da API da **Anthropic** (Claude).

## 3. Subindo a infraestrutura

```powershell
docker compose up -d
```

Isso sobe o Evolution API, o Postgres e o Redis.

## 4. Conectando o WhatsApp

Crie a instância:

```powershell
curl.exe -X POST -H "apikey: minha_chave_123" -H "Content-Type: application/json" `
  http://localhost:8080/instance/create `
  -d '{\"instanceName\":\"anamnese-bot\",\"integration\":\"WHATSAPP-BAILEYS\",\"qrcode\":true}'
```

Depois abra **http://localhost:8080/manager**, faça login com a API key e
escaneie o QR Code com o app do WhatsApp do número que será o bot.

## 5. Registrando o webhook

Aponta o Evolution para o FastAPI. O `host.docker.internal` permite que o
container alcance o servidor rodando na máquina host:

```powershell
curl.exe -X POST -H "apikey: minha_chave_123" -H "Content-Type: application/json" `
  http://localhost:8080/webhook/set/anamnese-bot `
  -d '{\"webhook\":{\"enabled\":true,\"url\":\"http://host.docker.internal:8000/webhook\",\"webhookByEvents\":false,\"webhookBase64\":false,\"events\":[\"MESSAGES_UPSERT\"]}}'
```

## 6. Indexando os PDFs do RAG

Lê os PDFs em `uploads/pdfs/` e gera o índice vetorial em `vector_store/`:

```powershell
python -m app.agent.rag
```

## 7. Rodando o bot

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

O `--host 0.0.0.0` é obrigatório: o Evolution roda em container e precisa
alcançar o FastAPI pelo `host.docker.internal`. A porta deve ser diferente da
8080 (usada pelo Evolution).

Pronto — qualquer mensagem enviada ao número conectado é respondida pelo bot.

## Estrutura do projeto

```
app/
  main.py            FastAPI + endpoint do webhook
  config.py          variáveis de ambiente
  agent/
    agent.py         agente conversacional (processa cada mensagem)
    prompt.py        prompt do sistema
    sections.py      definição das 9 seções da anamnese
    rag.py           indexação e consulta dos PDFs
  session/
    manager.py       estado da conversa por paciente (em memória)
  whatsapp/
    client.py        envio de mensagens via Evolution API
    webhook.py       parsing dos eventos recebidos
  docx/
    generator.py     geração do relatório .docx
uploads/pdfs/        PDFs de protocolos clínicos (fonte do RAG)
vector_store/        índice ChromaDB (gerado)
output/              relatórios .docx gerados
docker-compose.yml   Evolution API + Postgres + Redis
```

## Observações

- As sessões de anamnese ficam **em memória** — reiniciar o servidor zera
  todas as conversas em andamento.
- O bot responde qualquer mensagem que chega ao número conectado. Para uso
  real, recomenda-se um número dedicado, não um número pessoal.
