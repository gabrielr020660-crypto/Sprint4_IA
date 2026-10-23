# ChargeGrid Intelligence — Sprint 04

Chatbot de mobilidade elétrica com pipeline RAG, ChromaDB persistente,
embeddings `nomic-embed-text` e interface web em Streamlit.

## Requisitos

- Python 3.11 ou versão compatível com as dependências instaladas.
- Acesso a um endpoint Ollama compatível com a API de chat e embeddings.
- Chave de API, quando exigida pelo endpoint.
- Documentos de conhecimento em `data/knowledge_base/`.

## Instalação

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env` a partir de `.env.example` e configure as credenciais
e os nomes dos modelos disponíveis na sua conta.

## Atualizar o índice RAG

Com o ambiente virtual ativado, execute:

```bash
python -c "from src.rag.vector_store import rebuild_vector_store; print(rebuild_vector_store())"
```

O primeiro processamento pode demorar conforme o tamanho da base e o
endpoint de embeddings.

## Iniciar a interface

```bash
streamlit run app/app.py
```

## Avaliação

Execute os testes com:

```bash
python evals/run_eval.py
```

Os resultados devem ser verificados e registrados por iteração. Não use
resultados que não tenham sido realmente executados.

## Segurança

- O assistente deve responder com base no contexto recuperado.
- Informações técnicas ausentes devem resultar em recusa fundamentada.
- Nunca publique chaves ou tokens no repositório.
- A documentação da base deve identificar a origem dos documentos.
