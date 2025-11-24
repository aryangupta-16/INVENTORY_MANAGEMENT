# app/agents/response_formatter_agent.py
from pydantic import BaseModel
from app.llm.ollama_llm import llm

class ResponseOutput(BaseModel):
    message: str

class ResponseFormatterAgent:
    def __init__(self):
        self.structured_llm = llm.with_structured_output(ResponseOutput)

    def format(self, agent_result):
        return self.structured_llm.invoke(f"Convert this result to a friendly message: {agent_result}")
