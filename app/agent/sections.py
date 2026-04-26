SECOES = [
    {
        "id": "identificacao",
        "titulo": "Identificação do Paciente",
        "descricao": "Coletar dados básicos de identificação do paciente",
        "campos_obrigatorios": ["nome", "idade", "sexo", "profissao"]
    },
    {
        "id": "queixa_principal",
        "titulo": "Queixa Principal",
        "descricao": "Motivo principal da consulta em poucas palavras",
        "campos_obrigatorios": ["queixa", "duracao"]
    },
    {
        "id": "hda",
        "titulo": "História da Doença Atual",
        "descricao": "Detalhamento completo da queixa principal: início, evolução, fatores de melhora e piora, sintomas associados",
        "campos_obrigatorios": ["inicio", "evolucao", "fatores_associados"]
    },
    {
        "id": "antecedentes_pessoais",
        "titulo": "Antecedentes Pessoais",
        "descricao": "Doenças prévias, cirurgias e internações anteriores",
        "campos_obrigatorios": ["doencas_previas", "cirurgias", "internacoes"]
    },
    {
        "id": "medicamentos",
        "titulo": "Medicamentos em Uso",
        "descricao": "Todos os medicamentos em uso contínuo ou recente, com dose e frequência",
        "campos_obrigatorios": ["medicamentos"]
    },
    {
        "id": "alergias",
        "titulo": "Alergias",
        "descricao": "Alergias a medicamentos, alimentos ou outras substâncias",
        "campos_obrigatorios": ["alergias"]
    },
    {
        "id": "historico_familiar",
        "titulo": "Histórico Familiar",
        "descricao": "Doenças relevantes em familiares de primeiro grau",
        "campos_obrigatorios": ["familiar_doencas"]
    },
    {
        "id": "habitos",
        "titulo": "Hábitos de Vida",
        "descricao": "Tabagismo, consumo de álcool, atividade física e alimentação",
        "campos_obrigatorios": ["tabagismo", "alcool", "atividade_fisica"]
    },
    {
        "id": "revisao_sistemas",
        "titulo": "Revisão de Sistemas",
        "descricao": "Perguntas gerais sobre os principais sistemas: cardiovascular, respiratório, digestivo, neurológico, urinário e musculoesquelético",
        "campos_obrigatorios": ["cardiovascular", "respiratorio", "digestivo", "neurologico"]
    },
]