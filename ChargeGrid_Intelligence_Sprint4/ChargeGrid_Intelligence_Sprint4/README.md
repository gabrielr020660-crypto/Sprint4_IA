# ChargeGrid Intelligence — Sprint 04

Assistente de mobilidade elétrica baseado em RAG para o EV Challenge / GoodWe. O projeto carrega PDFs e TXT, divide o conteúdo em trechos, cria embeddings `nomic-embed-text`, persiste os vetores em ChromaDB e responde com fontes visíveis na interface Streamlit.

## Ambiente recomendado

- Python **3.11 ou 3.12** (não use o `.venv` antigo do ZIP; ele foi criado com Python 3.14).
- Endpoint Ollama local ou Ollama Cloud compatível com `/api/chat` e `/api/embed`.
- Chave em variável de ambiente; nunca publique `.env`.

## Instalação no Windows (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `.env` e configure a chave e os nomes de modelos disponíveis na sua conta. Para Ollama Cloud, use `https://ollama.com` tanto em `OLLAMA_BASE_URL` quanto em `OLLAMA_EMBED_BASE_URL`. Para Ollama local, use `http://localhost:11434` e confirme que os modelos estão disponíveis localmente.

## Atualizar a base e iniciar

```powershell
python -c "from src.rag.vector_store import rebuild_vector_store; print('Trechos indexados:', rebuild_vector_store())"
streamlit run app/app.py
```

Abra o endereço local mostrado pelo Streamlit. Sempre que mudar documentos em `data/knowledge_base/`, reconstrua o índice.

## Avaliação

```powershell
python evals/run_eval.py
```

O script grava um JSON com respostas e fontes. Depois, avalie manualmente cada resposta usando os critérios em `evals/rubrica_manual.md` e preencha as notas no JSON. Repita o mesmo conjunto de perguntas após alterar o prompt ou recuperação. **Não reporte médias nem melhoria antes de executar e revisar as duas iterações.**

## Estrutura principal

- `data/knowledge_base/`: PDFs e TXT usados como fonte.
- `src/rag/`: loader, chunking, embeddings, ChromaDB, recuperação e resposta.
- `prompts/`: histórico de versões do prompt RAG.
- `app/app.py`: interface Streamlit.
- `evals/`: conjunto fixo de avaliação, script e rubrica manual.
- `docs/`: relatórios da Sprint 04.

## Limitações conhecidas

- A recusa fora de escopo é uma regra conservadora baseada em palavras-chave; não substitui uma avaliação de segurança completa.
- A proteção contra prompt injection combina filtro básico na pergunta e instruções no prompt. Ela precisa ser testada e não deve ser descrita como infalível.
- O limiar de distância (`RAG_DISTANCE_THRESHOLD=1.2`) é um valor inicial e deve ser calibrado com as consultas de avaliação.
- A presença de uma citação indica os trechos recuperados, mas não garante sozinha que cada frase da resposta está sustentada; revise os resultados.
- A base inclui manuais em inglês e resumos/guias em português. Verifique a versão e a aplicabilidade de cada manual antes de usar uma especificação técnica.
