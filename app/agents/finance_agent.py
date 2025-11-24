# app/agents/finance_agent.py
from pydantic import BaseModel
from langchain.tools import Tool
from app.llm.ollama_llm import llm
from app.tools.finance_tools import get_balance, record_payment

class FinanceOutput(BaseModel):
    action: str
    customer: str
    amount: float = None

class FinanceAgent:
    def __init__(self):
        self.structured_llm = llm.with_structured_output(FinanceOutput)
        self.tools = [
            Tool(name="get_balance", func=get_balance, description="Check customer balance"),
            Tool(name="record_payment", func=record_payment, description="Record a payment")
        ]
        self.llm_with_tools = self.structured_llm.bind_tools(self.tools)

    def execute(self, user_input: str, db):
        return self.llm_with_tools.invoke(user_input)
