from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# load_dotenv(override=True)
# Raw LLM definition
llm = ChatOllama(model="llama3.1", temperature=0)

# llm = ChatOpenAI(model="gpt-4")