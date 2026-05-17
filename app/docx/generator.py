import json
import os
from datetime import datetime

from docx import Document
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

from app.config import ANTHROPIC
from app.agent.sections import SECOES

OUTPUT_DIR = "output"

llm = ChatAnthropic(model="claude-haiku-4-5", api_key=ANTHROPIC, max_tokens=4096)


def _extrair_json(texto):
    texto = texto.strip()
    inicio = texto.find("{")
    fim = texto.rfind("}")
    return json.loads(texto[inicio:fim + 1])


def _estruturar_anamnese(historico):
    """Usa o LLM para organizar a conversa nas seções da anamnese."""
    conversa = "\n".join(
        f"{'Paciente' if m['role'] == 'user' else 'Assistente'}: {m['content']}"
        for m in historico
    )
    secoes_desc = "\n".join(
        f"- {s['id']}: {s['titulo']} — {s['descricao']}" for s in SECOES
    )

    instrucoes = (
        "Você recebeu a transcrição de uma anamnese clínica feita por WhatsApp. "
        "Organize as informações coletadas nas seções abaixo.\n\n"
        f"SEÇÕES:\n{secoes_desc}\n\n"
        "Responda APENAS com um objeto JSON em que cada chave é o id da seção e "
        "o valor é um texto corrido, em português, com as informações daquela seção. "
        "Se alguma informação não foi coletada, escreva 'Não informado'. "
        "Não invente dados que não estejam na conversa."
    )

    resposta = llm.invoke([
        SystemMessage(content=instrucoes),
        HumanMessage(content=conversa),
    ])
    return _extrair_json(resposta.content)


def gerar_relatorio(telefone, historico):
    """Gera o relatório .docx da anamnese e retorna o caminho do arquivo."""
    dados = _estruturar_anamnese(historico)
    identificador = telefone.split("@")[0]

    doc = Document()
    doc.add_heading("Relatório de Anamnese", level=0)

    cabecalho = doc.add_paragraph()
    cabecalho.add_run("Paciente: ").bold = True
    cabecalho.add_run(identificador)
    cabecalho.add_run("\nData: ").bold = True
    cabecalho.add_run(datetime.now().strftime("%d/%m/%Y %H:%M"))

    for i, secao in enumerate(SECOES, start=1):
        doc.add_heading(f"{i}. {secao['titulo']}", level=1)
        doc.add_paragraph(str(dados.get(secao["id"], "Não informado")))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    nome = f"anamnese_{identificador}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    caminho = os.path.join(OUTPUT_DIR, nome)
    doc.save(caminho)

    return caminho
