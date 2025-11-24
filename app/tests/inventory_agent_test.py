# tests/test_inventory_agent.py
from app.agents.inventory_agent import InventoryAgent
from app.config.database import get_db  # however you create session

def test_inventory_agent():
    db = get_db()
    agent = InventoryAgent()

    user_query = "Can you give me all the products?"
    response = agent.handle_query(user_query)

    # print("Raw Result:", response["result"])
    print("LLM Response:", response)

if __name__ == "__main__":
    test_inventory_agent()
