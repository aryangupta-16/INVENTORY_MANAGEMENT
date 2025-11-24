from app.llm.ollama_llm import llm
from app.tools.inventory_tools import (
    check_stock,
    add_stock,
    reduce_stock,
    get_low_stock_products,
    get_all_products,
    get_product_by_id
)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage


# ✅ Bind all inventory tools directly to the LLM
llm_with_tools = llm.bind_tools([
    check_stock,
    add_stock,
    reduce_stock,
    get_low_stock_products,
    get_all_products,
    get_product_by_id
])


class InventoryAgent:
    def __init__(self):
        self.llm = llm_with_tools

        self.system_prompt = """
        You are an **Inventory Management AI Agent**.

        You have access to the following tools:
        - `check_stock(product_name: str, user_id: int)`
        - `add_stock(product_name: str, user_id: int, quantity: int)`
        - `reduce_stock(product_name: str, user_id: int, quantity: int)`
        - `get_low_stock_products(user_id: int)`
        - `get_all_products(user_id: int)`
        - `get_product_by_id(product_id: int, user_id: int)`

        Rules:
        1. You are responsible for managing products and stock.
        2. Always try to use tools when possible to fetch or modify data.
        3. If `user_id` is not given in the query, assume `user_id = 1`.
        4. Never invent data; if a tool gives an error, return that error message as-is.
        5. Always keep responses short, helpful, and action-oriented.

        Examples:
        - "Add 10 kg rice" → call `add_stock(product_name="rice", user_id=1, quantity=10)`
        - "How many apples are in stock?" → call `check_stock(product_name="apples", user_id=1)`
        - "Show all low stock products" → call `get_low_stock_products(user_id=1)`
        - "List all my products" → call `get_all_products(user_id=1)`
        - "Get details of product 3" → call `get_product_by_id(product_id=3, user_id=1)`
        """

    def handle_query(self, user_query: str):
        """
        Handles any inventory-related query.
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
