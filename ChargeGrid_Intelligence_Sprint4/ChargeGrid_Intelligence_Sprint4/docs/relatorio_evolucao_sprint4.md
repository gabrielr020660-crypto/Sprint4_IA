# Relatório de Evolução do Projeto — Sprint 04
## ChargeGrid Intelligence | FIAP — Prompt and Artificial Intelligence | 2026.2

### 1. Resumo da evolução

O ChargeGrid Intelligence evolui o chatbot conversacional anterior para um fluxo RAG que recupera evidências da base documental antes de gerar uma resposta. A Sprint 04 acrescenta persistência vetorial com ChromaDB, embeddings `nomic-embed-text`, citações de fontes na interface Streamlit, regras de grounding e um conjunto de avaliação reproduzível. A proposta é reduzir respostas sem evidência e facilitar a verificação pelo usuário.

### 2. Pipeline RAG e decisões

O loader lê arquivos PDF com `PyMuPDFLoader` e arquivos TXT com `TextLoader`, registrando o nome do documento como metadado de origem. `RecursiveCharacterTextSplitter` divide os documentos em trechos de 800 caracteres com overlap de 120. O tamanho busca manter contexto suficiente sem criar trechos muito grandes; a sobreposição reduz a chance de perder informação na fronteira entre trechos. O modelo `nomic-embed-text` gera os vetores e o ChromaDB os persiste em `chroma_db/`. O retriever retorna até três trechos (`top-k=3`), sujeitos a um limite inicial de distância de 1.2, que deve ser calibrado com as perguntas de avaliação.

### 3. Comparativo antes/depois

| Critério | Sprints 1/2 (versão original) | Sprint 04 (RAG avaliado) |
|---|---|---|
| Fluxo de resposta | Chatbot conversacional; respostas podiam depender do modelo | Recupera trechos antes da geração |
| Base documental | Sem recuperação vetorial demonstrada no fluxo original | PDFs e TXT carregados por loader |
| Banco vetorial | Não identificado como persistente no fluxo original | ChromaDB persistente |
| Citação de fonte | Não garantida no fluxo original | Fontes recuperadas exibidas na interface; revisar citação em cada resposta |
| Faithfulness — iteração 1 | Não há score histórico disponível nos arquivos revisados | Não medido nesta revisão: executar `evals/run_eval.py` e pontuar manualmente |
| Faithfulness — iteração 2 | Não há score histórico disponível nos arquivos revisados | Não medido nesta revisão: executar após mudança documentada |
| Answer relevancy — iteração 1 | Não há score histórico disponível nos arquivos revisados | Não medido nesta revisão |
| Answer relevancy — iteração 2 | Não há score histórico disponível nos arquivos revisados | Não medido nesta revisão |
| Interface web | Interface da Sprint 04 não demonstrada no fluxo anterior | Streamlit implementado em `app/app.py`; validar execução local |

### 4. Problemas encontrados e soluções

**Problema 1 — endpoint de embeddings diferente do endpoint de chat.** A configuração do projeto apontava embeddings para `http://localhost:11434`, apesar de o chat estar configurado para Ollama Cloud. Isso pode causar falha de conexão ou de indexação. A solução foi fazer o endpoint de embeddings herdar `OLLAMA_BASE_URL` por padrão e permitir autenticação Bearer quando a chave estiver configurada.

**Problema 2 — chave de API e ambiente local.** O arquivo compactado incluía `.env` e um ambiente virtual grande, inadequados para compartilhar. O pacote corrigido exclui `.env`, `.venv`, banco vetorial e histórico Git do ZIP. Como a chave pode ter sido registrada no histórico do repositório original, é importante revogá-la/rotacioná-la e limpar o histórico remoto antes da entrega pública.

**Problema 3 — risco de afirmações fora da base.** O prompt anterior não distinguia suficientemente a orientação geral de segurança de uma especificação oficial. O prompt v3 explicita grounding, citações, recusa por falta de evidência, escopo e tratamento de documentos como conteúdo não confiável.

**Problema 4 — avaliação sem números verificáveis.** Os relatórios anteriores continham conclusões não vinculadas a um conjunto de notas reproduzível. Foi incluída uma rubrica manual de 0–1 e mantido um conjunto fixo de oito casos. Os resultados precisam ser preenchidos após a execução real.

### 5. Avaliação e iterações

A avaliação usa `evals/eval_set.json` com oito casos: grounding, monitoramento, segurança elétrica, prompt injection, pergunta fora de escopo, tarifas não documentadas, citação e instrução maliciosa em documento. `evals/rubrica_manual.md` define critérios para `faithfulness` e `answer_relevancy`, ambos de 0 a 1, além do campo de segurança. A comparação deve usar o mesmo conjunto em duas iterações e só declarar ganho quando a segunda apresentar melhoria medida sem regressão nos casos de segurança.

### 6. Modelos e parâmetros

- Embeddings: `nomic-embed-text`.
- Modelo de geração: definido por `OLLAMA_CHAT_MODEL` (configuração de exemplo: `gemma4:31b-cloud`).
- Temperature: 0; top-p: 0.9; máximo de geração: 500 tokens.
- Chunk size: 800; overlap: 120; top-k: 3.
- Avaliação: rubrica manual equivalente documentada, devido à opção de fallback permitida no enunciado.

### 7. Equipe e divisão de trabalho

| Integrante | RM |
|---|---|---|
* Gustavo Guedes Pereira — RM 569779
* Lucas Angelo — RM 569530
* Gustavo de Souza — RM 570746
* Arthur Tae — RM 570647
* Gabriel Rodrigues — RM 569322
* Murillo Boyadjian - RM 570774

### 8. Conclusão

A Sprint 04 contém a estrutura de um pipeline RAG, uma interface Streamlit, fontes documentais e mecanismos iniciais de grounding e segurança. Antes de afirmar que a entrega está totalmente validada, ainda é necessário executar o rebuild do índice, testar a interface, realizar as duas iterações de avaliação, comparar dois modelos e preencher os resultados reais. A credencial exposta no ZIP original também deve ser rotacionada antes de tornar o repositório público.