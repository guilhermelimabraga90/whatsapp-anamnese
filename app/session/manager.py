from app.agent import sections

SECAO_PACIENTE = {
    "telefone": None, 
    "secao_atual": None,  
    "secoes_concluidas": [],                      
    "respostas" : {},
    "historico": []
}

SESSOES = {}

def criar_nova_secao(telefone):
    SESSOES[telefone] = {
    "telefone": telefone, 
    "secao_atual": sections.SECOES[0],  
    "secoes_concluidas": [],                      
    "respostas" : {},
    "historico": []
    }
    return SESSOES[telefone]

def buscar_secao(telefone):
    return SESSOES.get(telefone)

def atualizar_dados(secao,telefone):
    SESSOES[telefone] = secao

def avancar_proxima_secao(telefone):
    secao = buscar_secao(telefone)
    secao_atual = secao["secao_atual"]
    for i, secao in enumerate(sections.SECOES):
        if secao['id'] == secao_atual:
            SESSOES[telefone]["secoes_concluidas"].append(secao_atual)
            if i + 1 < len(sections.SECOES):
                SESSOES[telefone]["secao_atual"] = sections.SECOES[i + 1]
                return sections.SECOES[i + 1]
            return None