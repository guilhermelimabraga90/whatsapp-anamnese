import httpx
from app.config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE

API_URL = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}"

HEADERS = {
    "apikey": EVOLUTION_API_KEY,
    "Content-Type": "application/json"
}


async def enviar_mensagem(telefone, texto):
    """Envia mensagem de texto pelo WhatsApp via Evolution API"""
    payload = {
        "number": telefone,
        "text": texto
    }

    async with httpx.AsyncClient() as client:
        resposta = await client.post(API_URL, headers=HEADERS, json=payload)
        return resposta.json()
