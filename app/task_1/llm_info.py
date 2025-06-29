import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model


load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = init_chat_model(
    model = ChatGroq(model = "llama-3.3-70b-versatile")
)
