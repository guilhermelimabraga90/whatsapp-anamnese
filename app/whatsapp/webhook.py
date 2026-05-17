def extrair_mensagem(payload):
    """Extrai telefone e mensagem do payload do Evolution API"""
    try:
        if payload.get("event") != "messages.upsert":
            return None, None

        data = payload["data"]
        key = data["key"]

        if key.get("fromMe"):
            return None, None

        remote_jid = key["remoteJid"]

        if remote_jid.endswith("@g.us"):
            return None, None

        message = data.get("message", {})
        texto = (
            message.get("conversation")
            or message.get("extendedTextMessage", {}).get("text", "")
        )

        if not texto:
            return None, None

        return remote_jid, texto
    except (KeyError, IndexError, AttributeError):
        return None, None
