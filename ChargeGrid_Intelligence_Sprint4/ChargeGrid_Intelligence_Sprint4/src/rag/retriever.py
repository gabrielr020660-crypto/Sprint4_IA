import os
from dotenv import load_dotenv

from src.rag.vector_store import get_vector_store

load_dotenv()


def retrieve_context(question: str):
    """Retorna documentos relevantes e a distância calculada pelo Chroma."""
    store = get_vector_store()
    k = int(os.getenv("RAG_TOP_K", "3"))

    try:
        if store._collection.count() == 0:
            return []
    except Exception:
        # Let Chroma raise its own useful error if the collection is unavailable.
        pass

    results = store.similarity_search_with_score(
        question,
        k=max(1, min(k, 8)),
    )

    if not results:
        return []

    return [
        {
            "document": doc,
            "distance": float(distance),
            "source": doc.metadata.get("source", "Fonte não identificada"),
            "page": doc.metadata.get("page"),
        }
        for doc, distance in results
    ]