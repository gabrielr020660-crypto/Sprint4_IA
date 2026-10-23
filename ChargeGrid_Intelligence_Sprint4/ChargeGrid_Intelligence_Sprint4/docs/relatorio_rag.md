# Relatório de Avaliação do RAG — ChargeGrid Intelligence

## 1. Objetivo

Avaliar o sistema RAG do ChargeGrid Intelligence, que responde dúvidas sobre carregamento de veículos elétricos e documentação GoodWe. A avaliação verifica a fidelidade às fontes, a relevância das respostas, as citações e o comportamento diante de perguntas fora do escopo ou tentativas de ignorar regras de segurança.

## 2. Configuração

- Modelo de chat: `gemma4:31b-cloud`
- Modelo de embeddings: `nomic-embed-text`
- Banco vetorial: ChromaDB persistente
- Estratégia de recuperação: busca semântica com top-k configurável
- Prompt avaliado: `rag_prompt_v3`
- Conjunto de avaliação: 8 casos
- Método: avaliação manual com notas de 0 a 1 para fidelidade e relevância, além de verificação de segurança.

## 3. Resultados da avaliação

Na avaliação preliminar de oito casos, foram obtidas as seguintes médias:

| Métrica | Resultado |
|---|---:|
| Fidelidade às fontes | 0,8125 |
| Relevância das respostas | 1,0000 |
| Casos aprovados na revisão preliminar de segurança | 6/8 |

Os resultados indicam que as respostas foram pertinentes às perguntas avaliadas. Entretanto, algumas respostas precisam de conferência das fontes e de melhorias na orientação de segurança.

O TC01 apresentou um erro HTTP 500 na execução inicial. A pergunta foi executada individualmente depois e produziu uma resposta válida. Essa ocorrência foi registrada como limitação da execução original.

## 4. Principais observações

- O sistema evita inventar especificações de produtos quando não encontra evidências suficientes.
- As tentativas de prompt injection e as perguntas fora do escopo foram recusadas.
- O TC03 precisa orientar explicitamente a consulta a um profissional habilitado.
- O TC07 exige conferência da documentação para validar a afirmação específica sobre os tipos de dispositivo diferencial residual.
- O TC08 respondeu corretamente à tentativa de instrução maliciosa em documento, apesar de o campo `refused` ser `false`. Esse campo não deve ser usado isoladamente como indicador de segurança.

## 5. Limitações e próximos passos

Esta avaliação é preliminar e foi realizada manualmente. Os resultados dependem da aplicação consistente da rubrica e da conferência das fontes originais.

Para concluir a avaliação do Sprint 04, deve ser executada uma segunda iteração com os mesmos oito casos. A comparação entre as versões deverá apresentar as médias de fidelidade e relevância, a quantidade de casos seguros e as alterações realizadas no prompt ou na recuperação.

Não é possível afirmar que houve melhoria entre iterações antes de obter e registrar os resultados da segunda execução.