"""Conservative scope check for the EV charging knowledge assistant."""
import re

TOPIC_TERMS = {
    "carregamento", "carregador", "carregadores", "veículo", "veiculos",
    "elétrico", "eletrico", "recarga", "bateria", "energia", "kwh", "kw",
    "goodwe", "chargegrid", "ev", "hca", "instalação", "instalacao",
    "disjuntor", "aterramento", "tomada", "tarifa", "posto", "conector",
    "corrente", "tensão", "tensao", "potência", "potencia", "monitoramento",
    "carregar", "carrega", "segurança", "seguranca", "manual", "equipamento",
    "condomínio", "condominio", "estação", "estacao", "plug", "carga",
    "documento", "documentos", "instrução", "instrucoes", "instrução", "regras",
}


def validar_escopo(texto: str) -> bool:
    normalized = re.sub(r"[^a-zA-ZÀ-ÿ0-9]+", " ", texto.lower())
    words = set(normalized.split())
    return bool(words & TOPIC_TERMS)
