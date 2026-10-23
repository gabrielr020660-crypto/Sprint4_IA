from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

def consultar_multi_provider(mensagem: str):
    # Prompt 1: Resposta Direta
    prompt_tecnico = ChatPromptTemplate.from_template("Responda de forma técnica sobre GoodWe: {input}")
    # Prompt 2: Resposta Simplificada
    prompt_simples = ChatPromptTemplate.from_template("Explique de forma simples sobre GoodWe: {input}")

    # Modelo 1
    llm_principal = ChatOllama(model="gpt-oss:120b", temperature=0.1)
    # Modelo 2
    llm_secundario = ChatOllama(model="qwen3:8b", temperature=0.5)

    chain1 = prompt_tecnico | llm_principal
    chain2 = prompt_simples | llm_secundario

    res1 = chain1.invoke({"input": mensagem})
    res2 = chain2.invoke({"input": mensagem})

    return {
        "resposta_tecnica_gpt": res1.content,
        "resposta_simples_qwen": res2.content
    }