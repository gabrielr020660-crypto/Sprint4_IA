"""Embeddings via Ollama API (local or cloud), compatible with LangChain."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class OllamaCloudEmbeddings:
    """Embeddings nomic-embed-text via /api/embed, with optional Bearer auth."""

    def __init__(self):
        self.base_url = os.getenv(
            "OLLAMA_EMBED_BASE_URL",
            os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ).rstrip("/")
        self.api_key = os.getenv("OLLAMA_API_KEY", "").strip()
        self.model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
        self.timeout = int(os.getenv("OLLAMA_EMBED_TIMEOUT", "180"))

    def _embed(self, texts):
        if not texts:
            return []
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.post(
            f"{self.base_url}/api/embed",
            headers=headers,
            json={"model": self.model, "input": texts},
            timeout=self.timeout,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Falha na API de embeddings ({response.status_code}) em "
                f"{self.base_url}/api/embed. Confira URL, chave e modelo. "
                f"Detalhe: {response.text[:500]}"
            ) from exc
        data = response.json()
        vectors = data.get("embeddings", [])
        if len(vectors) != len(texts) or any(not v for v in vectors):
            raise ValueError("A API não retornou um embedding para cada texto.")
        return vectors

    def embed_documents(self, texts):
        return self._embed(texts)

    def embed_query(self, text):
        return self._embed([text])[0]
