from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 
from .prompt import SYSTEM_PROMPT
from app.config import ANTHROPIC
from app.session import manager


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=ANTHROPIC
)



def processar_mensagem(telefone, mensagem, prompt = SYSTEM_PROMPT):

    secao_manager = manager.buscar_secao(telefone)
    if secao_manager == None:
        secao_manager = manager.criar_nova_secao(telefone) 

    historico   = secao_manager["historico"]
    historico.append({"role":"HumanMessage", "content": mensagem })
    
    mensagens = [SystemMessage(content=prompt),]

    for historico_mensagem in historico:
        if historico_mensagem["role"] == "HumanMessage":
            mensagens.append(HumanMessage(content=historico_mensagem["content"]))
        else:
             mensagens.append(AIMessage(content=historico_mensagem["content"]))

    resposta_raw = llm.invoke(mensagens)

    reposta = resposta_raw.content

    historico.append({"role":"AIMessage", "content": reposta })

    if "[SECAO_CONCLUIDA]" in reposta:
        manager.avancar_proxima_secao(telefone)
    return reposta