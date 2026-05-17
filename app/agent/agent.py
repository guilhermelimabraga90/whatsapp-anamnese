from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.agent.prompt import SYSTEM_PROMPT
from app.config import ANTHROPIC
from app.session import manager
from app.agent.rag import consultar
from app.docx.generator import gerar_relatorio

llm = ChatAnthropic(
    model="claude-haiku-4-5",
    api_key=ANTHROPIC,
    max_tokens=2048
)


def processar_mensagem(telefone, mensagem):
    secao_manager = manager.buscar_secao(telefone)
    if secao_manager is None:
        secao_manager = manager.criar_nova_secao(telefone)

    historico = secao_manager["historico"]

    contexto_rag = consultar(mensagem)

    prompt_completo = SYSTEM_PROMPT.replace("{contexto_rag}", contexto_rag)

    historico.append({"role": "user", "content": mensagem})

    mensagens = [SystemMessage(content=prompt_completo)]

    for item in historico:
        if item["role"] == "user":
            mensagens.append(HumanMessage(content=item["content"]))
        else:
            mensagens.append(AIMessage(content=item["content"]))

    resposta_raw = llm.invoke(mensagens)
    resposta = resposta_raw.content

    historico.append({"role": "assistant", "content": resposta})

    if "[SECAO_CONCLUIDA]" in resposta:
        manager.avancar_proxima_secao(telefone)
        resposta = resposta.replace("[SECAO_CONCLUIDA]", "").strip()

    if "[ANAMNESE_CONCLUIDA]" in resposta:
        resposta = resposta.replace("[ANAMNESE_CONCLUIDA]", "").strip()
        gerar_relatorio(telefone, historico)

    return resposta