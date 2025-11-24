# app/agents/business_agent.py

from app.agents.inventory_agent import InventoryAgent
from app.agents.customer_agent import CustomerAgent
from app.llm.ollama_llm import llm
from langchain_core.messages import SystemMessage, HumanMessage

class RouterAgent:
    def __init__(self):
        self.inventory_agent = InventoryAgent()
        self.customer_agent = CustomerAgent()
        self.llm_router = llm  # LLM instance for routing queries

        self.system_prompt = """
        You are a **Business Query Router**. 
        Decide whether a user's query should go to the InventoryAgent or the CustomerAgent.
        Rules:
        1. Queries about products, stock, or inventory → InventoryAgent
        2. Queries about customers, purchases, or customer info → CustomerAgent
        3. Only return the agent name as 'inventory' or 'customer'. 
        Example: 
        - "Add 10 apples" → inventory
        - "Create new customer John" → customer
        """

    def handle_query(self, user_query: str):
        # Step 1: Ask LLM to decide the agent
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_query)
        ]
        routing_response = self.llm_router.invoke(messages)
        agent_choice = (routing_response.content or "").strip().lower()

        # Step 2: Forward to the chosen agent
        if "inventory" in agent_choice:
            return self.inventory_agent.handle_query(user_query)
        elif "customer" in agent_choice:
            return self.customer_agent.handle_query(user_query)
        else:
            return "❌ Sorry, I couldn't determine which agent should handle your query."
