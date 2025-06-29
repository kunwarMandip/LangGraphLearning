
from langchain_groq import ChatGroq
from app.task_1.ai_prompt import prompt
from langgraph.prebuilt import create_react_agent

agent= create_react_agent(
    model = ChatGroq(model = "llama-3.3-70b-versatile"),
    prompt = prompt
)