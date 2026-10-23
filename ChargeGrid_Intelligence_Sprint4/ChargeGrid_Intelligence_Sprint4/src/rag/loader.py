from pathlib import Path

from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
)

BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge_base"


def load_documents():
    """Carrega PDFs e arquivos TXT da base de conhecimento."""
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    documents = []

    for path in KNOWLEDGE_DIR.rglob("*.pdf"):
        try:
            loaded = PyMuPDFLoader(str(path)).load()
            for doc in loaded:
                doc.metadata["source"] = path.name
            documents.extend(loaded)
        except Exception as exc:
            print(f"[AVISO] Não foi possível ler {path.name}: {exc}")

    for path in KNOWLEDGE_DIR.rglob("*.txt"):
        try:
            loaded = TextLoader(str(path), encoding="utf-8").load()
            for doc in loaded:
                doc.metadata["source"] = path.name
            documents.extend(loaded)
        except Exception as exc:
            print(f"[AVISO] Não foi possível ler {path.name}: {exc}")

    if not documents:
        raise RuntimeError(
            "A base está vazia. Adicione pelo menos um PDF ou TXT em "
            "data/knowledge_base/."
        )

    return documents