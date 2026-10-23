# Relatório de Modelos — ChargeGrid Intelligence

## 1. Objetivo

Este relatório registra os modelos utilizados no ChargeGrid Intelligence e os parâmetros relevantes para a execução do sistema RAG.

## 2. Modelos utilizados

| Componente | Modelo | Função |
|---|---|---|
| Chat | `gemma4:31b-cloud` | Geração de respostas com base no contexto recuperado |
| Embeddings | `nomic-embed-text` | Transformação dos documentos e perguntas em vetores para busca semântica |

O projeto utiliza a API do Ollama Cloud para acessar os modelos. A recuperação de documentos é realizada pelo ChromaDB persistente.

## 3. Parâmetros de execução

| Parâmetro | Configuração conhecida |
|---|---|
| `RAG_TOP_K` | 5 |
| `RAG_DISTANCE_THRESHOLD` | 1.2 |
| Versão do prompt avaliada | `rag_prompt_v3` |

Os parâmetros de geração, como temperatura, `top_p` e limite de tokens, devem ser confirmados no código da chamada ao modelo antes de registrar seus valores definitivos.

## 4. Comparação e limitações

O modelo de chat é responsável pela geração da resposta, enquanto o modelo de embeddings permite recuperar trechos relevantes da base documental.

Ainda não há resultados comparativos suficientes para afirmar que um segundo modelo de chat apresenta desempenho superior. Uma comparação válida deve utilizar o mesmo conjunto de perguntas, os mesmos critérios de avaliação e configurações documentadas.

## 5. Conclusão

A configuração atual combina recuperação semântica com geração condicionada ao contexto documental. A principal preocupação é manter as respostas fundamentadas nas fontes, evitar especificações inventadas e recusar instruções que contrariem as regras de segurança.

Para uma comparação quantitativa entre modelos, será necessário registrar os modelos adicionais testados e suas respectivas métricas.