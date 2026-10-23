from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """Divide os documentos em trechos com sobreposição."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)