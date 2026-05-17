from fastapi import FastAPI, Request
from app.whatsapp.webhook import extrair_mensagem
from app.whatsapp.client import enviar_mensagem
from app.agent.agent import processar_mensagem

app = FastAPI()


@app.post("/webhook")
async def receber_mensagem(request: Request):
    """Recebe eventos do WhatsApp via Evolution API"""
    payload = await request.json()
    telefone, texto = extrair_mensagem(payload)

    if telefone and texto:
        resposta = processar_mensagem(telefone, texto)
        await enviar_mensagem(telefone, resposta)

    return {"status": "ok"}
