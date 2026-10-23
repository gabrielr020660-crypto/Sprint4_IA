from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from src.chain.memoria import get_session_history
from src.guardrails.scope_validator import validar_escopo
from src.guardrails.moderation import checar_jailbreak

def build_ev_chain(model_name: str = "gemma:2b", temperature: float = 0.2):
    llm = ChatOllama(model=model_name, temperature=temperature)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é o assistente virtual GoodWe Brasil sobre Mobilidade Elétrica."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = prompt | llm
    
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    return chain_with_history

def invocar_chatbot(session_id: str, mensagem: str):
    if checar_jailbreak(mensagem):
        return "Sua mensagem contém instruções não permitidas por motivos de segurança."
    
    if not validar_escopo(mensagem):
        return "Desculpe, sou um assistente focado em soluções de mobilidade elétrica GoodWe. Como posso te ajudar nesse tema?"
        
    chain = build_ev_chain()
    response = chain.invoke(
        {"input": mensagem},
        config={"configurable": {"session_id": session_id}}
    )
    return response.content