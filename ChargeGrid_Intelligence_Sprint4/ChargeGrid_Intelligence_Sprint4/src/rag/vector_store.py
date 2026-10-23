from pathlib import Path

from langchain_chroma import Chroma

from src.rag.embeddings import OllamaCloudEmbeddings
from src.rag.loader import load_documents
from src.rag.chunking import split_documents

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "chargegrid_knowledge"


def get_vector_store():
    """Abre o banco vetorial persistente existente."""
    embeddings = OllamaCloudEmbeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )


def rebuild_vector_store():
    """Recria a coleção com os arquivos atuais da base."""
    documents = load_documents()
    chunks = split_documents(documents)
    if not chunks:
        raise RuntimeError("Os documentos foram carregados, mas não geraram trechos para indexação.")
    embeddings = OllamaCloudEmbeddings()

    store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    # Limpa os registros anteriores para não duplicar trechos.
    existing = store.get()
    ids = existing.get("ids", [])
    if ids:
        store.delete(ids=ids)

    store.add_documents(chunks)
    return len(chunks)