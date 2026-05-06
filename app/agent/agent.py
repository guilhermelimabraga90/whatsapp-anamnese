from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from .prompt import SYSTEM_PROMPT
from app.config import ANTHROPIC


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=ANTHROPIC
)



def processar_mensagem(telefone, mensagem, prompt = SYSTEM_PROMPT):
    mensagens = [
    SystemMessage(content=prompt),
    HumanMessage(content="mensagem")
    ]
    
