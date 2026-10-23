import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag.answer import answer_question
from src.rag.vector_store import rebuild_vector_store


st.set_page_config(
    page_title="ChargeGrid Intelligence",
    page_icon="⚡",
    layout="centered",
)

st.title("⚡ ChargeGrid Intelligence")
st.caption("Assistente de mobilidade elétrica com respostas baseadas em documentos.")

with st.sidebar:
    st.subheader("Base de conhecimento")
    st.write(
        "As respostas dependem dos documentos existentes em "
        "`data/knowledge_base/`."
    )
    if st.button("Atualizar índice de documentos"):
        try:
            with st.spinner("Lendo documentos e atualizando o ChromaDB..."):
                total = rebuild_vector_store()
            st.success(f"Índice atualizado: {total} trechos.")
        except Exception as exc:
            st.error(f"Falha ao atualizar o índice: {exc}")

question = st.text_area(
    "Digite sua dúvida sobre carregamento de veículos elétricos",
    placeholder="Ex.: O que a documentação informa sobre monitoramento?",
    height=100,
)

if st.button("Consultar", type="primary"):
    if not question.strip():
        st.warning("Digite uma pergunta antes de consultar.")
    else:
        try:
            with st.spinner("Consultando a base de conhecimento..."):
                result = answer_question(question.strip())

            st.subheader("Resposta")
            st.write(result["answer"])

            if result["sources"]:
                st.subheader("Fontes recuperadas")
                for source in result["sources"]:
                    st.write(
                        f"- {source['citation']} "
                        f"(distância: {source['distance']})"
                    )
            else:
                st.info("Nenhuma fonte foi considerada suficiente.")

            st.caption(
                f"Prompt utilizado: {result['prompt_version']} | "
                f"Recusa: {'sim' if result['refused'] else 'não'}"
            )

        except Exception as exc:
            st.error(
                "Não foi possível concluir a consulta. Verifique o arquivo "
                ".env, a disponibilidade do modelo e a configuração do ChromaDB."
            )
            st.code(str(exc))

st.divider()
st.caption(
    "Este protótipo é informativo. Não substitui manuais oficiais, "
    "projeto elétrico ou avaliação de profissional habilitado."
)