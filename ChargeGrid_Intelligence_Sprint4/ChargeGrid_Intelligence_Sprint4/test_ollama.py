
import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("OLLAMA_BASE_URL", "https://ollama.com").rstrip("/")
api_key = os.getenv("OLLAMA_API_KEY", "")
chat_model = os.getenv("OLLAMA_CHAT_MODEL", "gemma3:latest")
embed_model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

if not api_key or api_key == "COLOQUE_SUA_CHAVE_REAL_AQUI":
    raise SystemExit(
        "ERRO: a chave não foi configurada corretamente no .env."
    )

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

print("1. Testando modelo de conversa...")

try:
    response = requests.post(
        f"{base_url}/api/chat",
        headers=headers,
        json={
            "model": chat_model,
            "messages": [
                {
                    "role": "user",
                    "content": "Responda somente: CONEXAO_OK",
                }
            ],
            "stream": False,
        },
        timeout=120,
    )

    if response.ok:
        data = response.json()
        answer = data.get("message", {}).get("content", "")
        print("CHAT OK:", answer)
    else:
        print("ERRO NO CHAT:", response.status_code)
        print(response.text[:1000])

except requests.RequestException as exc:
    print("FALHA DE REDE NO CHAT:", str(exc))

print("\n2. Testando modelo de embeddings...")

try:
    response = requests.post(
        f"{base_url}/api/embed",
        headers=headers,
        json={
            "model": embed_model,
            "input": ["Teste de embeddings para o projeto ChargeGrid."]
        },
        timeout=120,
    )

    if response.ok:
        data = response.json()
        vectors = data.get("embeddings", [])
        if vectors and vectors[0]:
            print("EMBEDDINGS OK. Dimensões:", len(vectors[0]))
        else:
            print("A API respondeu, mas não retornou embeddings.")
    else:
        print("ERRO NOS EMBEDDINGS:", response.status_code)
        print(response.text[:1000])

except requests.RequestException as exc:
    print("FALHA DE REDE NOS EMBEDDINGS:", str(exc))

print("\n3. Verificando configuração (sem exibir a chave)...")
print("Base URL:", base_url)
print("Chave carregada:", bool(api_key))
print("Tamanho da chave:", len(api_key))
print("Modelo de chat:", chat_model)
print("Modelo de embeddings:", embed_model)

print("\n4. Testando endpoint OpenAI-compatible de embeddings...")

try:
    response = requests.post(
        f"{base_url}/v1/embeddings",
        headers=headers,
        json={
            "model": embed_model,
            "input": "Teste de embeddings para o projeto ChargeGrid."
        },
        timeout=120,
    )

    print("STATUS:", response.status_code)

    if response.ok:
        data = response.json()
        print("RESPOSTA OK:", "data" in data)
        if data.get("data"):
            print("DIMENSÕES:", len(data["data"][0]["embedding"]))
    else:
        print(response.text[:1000])

except requests.RequestException as exc:
    print("FALHA DE REDE:", str(exc))