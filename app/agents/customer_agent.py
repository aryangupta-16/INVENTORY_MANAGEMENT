"""
Customer Agent — LLM-driven agent for managing customers and purchases.

The agent decides which customer tool to call based on user queries
and provides summarized responses.
"""

from app.llm.ollama_llm import llm
from app.tools.customer_tools import (
    create_new_customer,
    remove_customer,
    fetch_all_customers,
    fetch_customer_by_phone,
    record_purchase,
    fetch_customer_purchases
)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage


# ✅ Bind all customer tools directly to the LLM
llm_with_tools = llm.bind_tools([
    create_new_customer,
    remove_customer,
    fetch_all_customers,
    fetch_customer_by_phone,
    record_purchase,
    fetch_customer_purchases
])


class CustomerAgent:
    def __init__(self):
        self.llm = llm_with_tools

        self.system_prompt = """
        You are a **Customer Management AI Agent**.

        You have access to the following tools:
        - `create_new_customer(user_id: int, customer_data: dict)`
        - `remove_customer(user_id: int, customer_id: int)`
        - `fetch_all_customers(user_id: int)`
        - `fetch_customer_by_phone(user_id: int, phone: str)`
        - `record_purchase(user_id: int, customer_id: int, product_id: int, quantity: int, paid: int)`
        - `fetch_customer_purchases(user_id: int)`

        Rules:
        1. Always try to use tools to fetch or modify data.
        2. Assume `user_id = 1` if not provided.
        3. Never invent data; if a tool fails, return the error message as-is.
        4. Keep responses concise, helpful, and actionable.

        Examples:
        - "Add a new customer John Doe with phone 9876543710" → call `create_new_customer(user_id=1, customer_data={"name": "John Doe", "phone": "9876543210","email":"johndoe@gmail.com"})`
        - "Delete customer 3" → call `remove_customer(user_id=1, customer_id=3)`
        - "Show all my customers" → call `fetch_all_customers(user_id=1)`
        - "Get purchases of all customers" → call `fetch_customer_purchases(user_id=1)`
        - "Record a purchase of 5 apples for customer 2, paid 200" → call `record_purchase(user_id=1, customer_id=2, product_id=<id>, quantity=5, paid=200)`
        """

    def handle_query(self, user_query: str):
        """
        Handles any customer-related query.
        LLM decides whether to call a tool, we execute it, and then LLM summarizes the result.
        """
        print(f"🔍 User Query: {user_query}")

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_query)
        ]

        # Step 1: Ask LLM what to do
        first_response = self.llm.invoke(messages)
        print(f"🧠 Raw LLM Response: {first_response}")

        tool_calls = getattr(first_response, "tool_calls", None)

        # Step 2: If LLM gives final text (no tool call)
        if not tool_calls:
            print("🤖 LLM Final Response:", first_response.content)
            return first_response.content

        # Step 3: Execute tool(s)
        tool_results = []
        for call in tool_calls:
            tool_name = call["name"]
            args = call["args"]
            tool_id = call["id"]

            print(f"🧩 Tool Call -> {tool_name}({args})")

            tool_func = globals().get(tool_name)
            if not tool_func:
                result = {"error": f"Tool '{tool_name}' not found"}
            else:
                try:
                    result = tool_func(**args)
                except Exception as e:
                    result = {"error": str(e)}

            print(f"✅ Tool Result: {result}")
            tool_results.append(ToolMessage(content=str(result), tool_call_id=tool_id))

        # Step 4: Send the tool results back to LLM for summarization
        followup_messages = messages + [AIMessage(content="", tool_calls=tool_calls)] + tool_results

        final_response = self.llm.invoke(followup_messages)
        print("🧾 Final Response:", final_response.content)

        return final_response.content
