# app/agents/command_validator_agent.py
from pydantic import BaseModel
from typing import Dict, Optional, List
from app.llm.ollama_llm import llm  # your Ollama LLM instance

class ValidatedCommand(BaseModel):
    action: str
    target_agent: str
    parameters: Dict[str, Optional[str]] = {}
    suggestions: Optional[List[str]] = None

# Define required parameters for each action
ACTION_PARAMETERS_MAP = {
    # Product / Inventory
    "add_product": ["product", "quantity", "price", "unit"],
    "update_product": ["product_id"],
    "delete_product": ["product_id"],
    "check_stock": ["product"],
    "low_stock_alert": [],
    "list_products": [],

    # Customer
    "add_customer": ["name", "email", "phone"],
    "update_customer": ["customer_id"],
    "delete_customer": ["customer_id"],
    "list_customers": [],
    "get_customer_by_phone": ["phone"],

    # Purchases
    "record_purchase": ["customer", "product", "quantity", "paid"],
    "list_customer_purchases": ["customer"],
    "get_purchase_details": ["purchase_id"],

    # Payments
    "record_payment": ["customer", "amount"],
    "get_pending_amount": ["customer"],
    "list_payments": []
}

class CommandValidatorAgent:
    def __init__(self):
        # LLM for filling missing fields and generating suggestions
        self.llm_with_tools = llm

        # Prepare system prompt template
        self.system_prompt_template = """
You are a **Command Validator Agent** for an inventory management system.

Inputs:
- action: The action the user wants to perform (e.g., add_product, record_payment, record_purchase)
- target_agent: The agent responsible for executing the action (e.g., inventory, customer, finance)
- user_input: The original message from the user
- required_parameters: A list of parameters required for this action

Your tasks:
1. Carefully analyze the user_input and extract values for all required parameters **Try to fill the required details correctly if you think they are right**.
2. For any required parameters **not mentioned**, add a question in `suggestions` asking the user to provide it.
3. Generate a JSON object with the following keys:
    - action: same as input
    - target_agent: same as input
    - parameters: dictionary containing all explicitly mentioned parameters
    - suggestions: list of questions for missing parameters
4. Do NOT invent or assume values for missing parameters.
5. Only output strictly valid JSON. Do not include explanations, markdown, or any extra text.

Example:

User input: "John Doe paid 200 today"

Action: record_payment  
Target Agent: finance  
Required Parameters: ["customer", "amount"]

Expected output:
{
  "action": "record_payment",
  "target_agent": "finance",
  "parameters": {
      "customer": "John Doe",
      "amount": "200"
  },
  "suggestions": []
}

Another example:

User input: "A payment was made"

Action: record_payment  
Target Agent: finance  
Required Parameters: ["customer", "amount"]

Expected output:
{
  "action": "record_payment",
  "target_agent": "finance",
  "parameters": {},
  "suggestions": ["Please provide the customer name.", "Please provide the payment amount."]
}

"""

    def validate(self, action: str, target_agent: str, user_input: str) -> ValidatedCommand:
        required_parameters = ACTION_PARAMETERS_MAP.get(action, [])

        # Build prompt for LLM
        prompt = f"{self.system_prompt_template}\nAction: {action}\nTarget Agent: {target_agent}\nRequired Parameters: {required_parameters}\nUser Input: \"{user_input}\""

        # Invoke LLM with structured output
        structured_llm = self.llm_with_tools.with_structured_output(ValidatedCommand)
        validated_command = structured_llm.invoke(prompt)

        return validated_command
