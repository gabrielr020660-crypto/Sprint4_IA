
import requests

url = "http://localhost:11434/api/embed"

payload = {
    "model": "nomic-embed-text",
    "input": "Teste de embeddings para o projeto ChargeGrid."
}

try:
    response = requests.post(url, json=payload, timeout=120)
    print("STATUS:", response.status_code)

    if response.ok:
        data = response.json()
        embeddings = data.get("embeddings", [])

        if embeddings and embeddings[0]:
            print("EMBEDDINGS OK!")
            print("Dimensões:", len(embeddings[0]))
        else:
            print("A API respondeu, mas não retornou vetores.")
    else:
        print(response.text[:1000])

except requests.RequestException as exc:
    print("Não foi possível conectar ao Ollama local:", exc)
