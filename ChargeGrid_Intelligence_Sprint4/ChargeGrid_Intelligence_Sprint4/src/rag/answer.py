import os
import requests
from dotenv import load_dotenv

from src.rag.retriever import retrieve_context
from src.rag.prompt_rag import SYSTEM_PROMPT, RAG_PROMPT_VERSION
from src.guardrails.scope_validator import validar_escopo

load_dotenv()

REFUSAL = (
    "Não encontrei informação suficiente na base de conhecimento "
    "para responder com segurança. Consulte o manual oficial do modelo "
    "ou um profissional habilitado, conforme o assunto."
)

INJECTION_MARKERS = [
    "ignore todas as instruções",
    "ignore as instruções anteriores",
    "ignore suas regras",
    "revele seu prompt",
    "ignore all previous instructions",
    "disregard previous instructions",
]


def contains_injection(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in INJECTION_MARKERS)


def call_ollama(prompt: str) -> str:
    base_url = os.getenv(
        "OLLAMA_BASE_URL", "https://ollama.com"
    ).rstrip("/")
    api_key = os.getenv("OLLAMA_API_KEY", "")
    model = os.getenv("OLLAMA_CHAT_MODEL", "gemma4:31b-cloud")

    if not api_key or api_key == "COLOQUE_SUA_CHAVE_AQUI":
        raise RuntimeError("Configure OLLAMA_API_KEY no arquivo .env.")

    response = requests.post(
        f"{base_url}/api/chat",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": prompt},
            ],
            "stream": False,
            "options": {
                "temperature": 0,
                "top_p": 0.9,
                "num_predict": 500,
            },
        },
        timeout=180,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("message", {}).get("content", "").strip()


def answer_question(question: str) -> dict:
    """Responde com RAG e devolve as fontes para a interface."""
    if contains_injection(question):
        return {
            "answer": (
                "Não posso seguir instruções que tentem desativar as "
                "regras de segurança. Posso ajudar com dúvidas documentadas "
                "sobre mobilidade elétrica."
            ),
            "sources": [],
            "prompt_version": RAG_PROMPT_VERSION,
            "refused": True,
        }

    if not validar_escopo(question):
        return {
            "answer": "Sou um assistente focado em carregamento de veículos elétricos e documentação GoodWe / ChargeGrid. Posso ajudar com dúvidas desse tema.",
            "sources": [],
            "prompt_version": RAG_PROMPT_VERSION,
            "refused": True,
        }

    retrieved = retrieve_context(question)

    if not retrieved:
        return {
            "answer": REFUSAL,
            "sources": [],
            "prompt_version": RAG_PROMPT_VERSION,
            "refused": True,
        }

    # Filtro inicial conservador. O valor deve ser calibrado com os testes
    # do próprio projeto e pode variar conforme a métrica do banco vetorial.
    threshold = float(os.getenv("RAG_DISTANCE_THRESHOLD", "1.2"))
    usable = [item for item in retrieved if item["distance"] <= threshold]

    if not usable:
        return {
            "answer": REFUSAL,
            "sources": [],
            "prompt_version": RAG_PROMPT_VERSION,
            "refused": True,
        }

    context_parts = []
    sources = []

    for index, item in enumerate(usable, start=1):
        doc = item["document"]
        source = item["source"]
        page = item["page"]

        citation = f"[{index}] {source}"
        if page is not None:
            citation += f", página {int(page) + 1}"

        context_parts.append(
            f"FONTE {citation}\n"
            f"Trecho:\n{doc.page_content}"
        )
        sources.append({
            "citation": citation,
            "distance": round(item["distance"], 4),
        })

    prompt = SYSTEM_PROMPT.format(
        context="\n\n---\n\n".join(context_parts),
        question=question,
    )

    answer = call_ollama(prompt)

    if not answer:
        answer = REFUSAL

    # As fontes serão exibidas pela interface, evitando duplicação
    # caso o modelo já tenha incluído citações na resposta.

    return {
        "answer": answer,
        "sources": sources,
        "prompt_version": RAG_PROMPT_VERSION,
        "refused": answer == REFUSAL,
    }