from agent import sections

SECAO_PACIENTE = {
    "telefone": None, 
    "secao_atual": None,  
    "secoes_concluidas": [],                      
    "respostas" : {}
}

SESSOES = {}

def criar_nova_secao(telefone):
    SESSOES[telefone] = {
    "telefone": telefone, 
    "secao_atual": None,  
    "secoes_concluidas": [],                      
    "respostas" : {}
    }
    return SESSOES[telefone]

def buscar_secao(telefone):
    return SESSOES.get(telefone)

def atualizar_dados(secao,telefone):
    SESSOES[telefone] = secao

def avancar_proxima_secao(secao_atual, telefone):
    proxima_secao = False
    lista_secao = sections.SECOES
    for secao in lista_secao:
        if proxima_secao:
            secao_aux = SESSOES[telefone]
            secao_aux["secao_atual"] = secao
            SESSOES[telefone] = secao_aux
            return secao
        if secao['id'] == secao_atual:
            SESSOES[telefone]["secoes_concluidas"].append(secao_atual)
            proxima_secao = True