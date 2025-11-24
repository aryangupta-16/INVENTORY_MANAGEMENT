# app/agents/command_interpreter_agent.py
from pydantic import BaseModel
from typing import Optional
from app.llm.ollama_llm import llm  # your Ollama LLM instance

class CommandOutput(BaseModel):
    action: Optional[str] = None           # e.g., add_product, record_purchase, etc.
    target_agent: Optional[str] = None     # inventory, customer, finance
    confirmation: Optional[str] = None     # Only populated if unsure about action

# Allowed actions mapped to their target agents
ACTION_AGENT_MAP = {
    # Product / Inventory Actions
    "add_product": "inventory",
    "update_product": "inventory",
    "delete_product": "inventory",
    "check_stock": "inventory",
    "low_stock_alert": "inventory",
    "list_products": "inventory",

    # Customer Actions
    "add_customer": "customer",
    "update_customer": "customer",
    "delete_customer": "customer",
    "list_customers": "customer",
    "get_customer_by_phone": "customer",

    # Purchases / Sales Actions
    "record_purchase": "customer",
    "list_customer_purchases": "customer",
    "get_purchase_details": "customer",

    # Payments / Finance Actions
    "record_payment": "finance",
    "get_pending_amount": "finance",
    "list_payments": "finance"
}


class CommandInterpreterAgent:
    def __init__(self):
        # LLM with structured output
        self.structured_llm = llm.with_structured_output(CommandOutput)
        self.llm_with_tools = self.structured_llm  # No tools needed for command parsing

        allowed_actions = ", ".join(ACTION_AGENT_MAP.keys())
        allowed_agents = set(ACTION_AGENT_MAP.values())

        self.system_prompt = f"""
You are a **Command Interpreter Agent** for an inventory management system.

Your job:
- Read a user's instruction.
- Identify exactly which **action** the user wants to perform.
- Identify the **target agent** responsible for that action.
- Only handle action determination; do NOT handle parameters.
- If you are not confident about the action, output a confirmation question instead of guessing.

Rules:
1. Only output JSON with keys: "action", "target_agent", optionally "confirmation".
2. Only choose actions from: {allowed_actions}.
3. Only choose target_agent from: {', '.join(allowed_agents)}.
4. If unsure about the action, set "action" and "target_agent" to null and include a "confirmation" field asking the user to clarify.
5. DO NOT hallucinate parameters or invent actions.
6. Output strictly valid JSON according to the CommandOutput schema.
7. Do not include explanations, markdown, or extra text.

Example when confident:
User: "Add 2kg of rice to inventory"
Output:
{{
  "action": "add_product",
  "target_agent": "inventory"
}}

Example when unsure:
User: "Add some items"
Output:
{{
  "action": null,
  "target_agent": null,
  "confirmation": "I am not sure what action you want to perform. Could you clarify if you want to add a product, record a purchase, or record a payment?"
}}
"""

    def parse(self, user_input: str):
        prompt = f"{self.system_prompt}\nUser input: \"{user_input}\""
        return self.llm_with_tools.invoke(prompt)
