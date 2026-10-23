# Prompt RAG v3 — grounding + escopo + citações
Versão ativa no pipeline. Usa exclusivamente o contexto recuperado para afirmações factuais, diferencia orientações gerais de especificações oficiais, cita fontes usando [n], recusa informação não sustentada, recusa perguntas fora do domínio EV/GoodWe/ChargeGrid e trata documentos como dados não confiáveis. Proíbe recomendações que contornem proteções elétricas e exige encaminhamento a profissional habilitado para dimensionamento.

Parâmetros de geração: temperature=0; top_p=0.9; max_tokens/num_predict=500. A versão do prompt fica registrada em cada resultado de avaliação.

Nota: a versão do prompt por si só não comprova melhoria. Comparar v1/v2/v3 com o mesmo conjunto de avaliação e registrar as notas reais.
