# app/graph/graph_builder.py

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage

from app.agents.router_agent import RouterAgent
from app.agents.customer_agent import CustomerAgent
from app.agents.inventory_agent import InventoryAgent
from typing import TypedDict

class AgenticState(TypedDict, total=False):
    user_input: str
    user_id: int
    agent_type: str
    tool_calls: list
    tool_results: list
    agent_response: str
    logs: list
# ------------------ Nodes ------------------

def router_node(state: AgenticState):
    """
    Uses RouterAgent to decide which agent should handle the query.
    """
    router = RouterAgent()
    user_query = state["user_input"]

    state["logs"].append("RouterAgent invoked")
    result = router.llm_router.invoke([
        HumanMessage(content=f"Decide agent: {user_query}")
    ])

    decision = result.content.strip().lower()
    state["agent_type"] = "customer" if "customer" in decision else "inventory"
    state["logs"].append(f"Router decided -> {state['agent_type']}")
    return state


def customer_agent_node(state: AgenticState):
    """
    Handles customer-related queries using CustomerAgent.
    """
    customer_agent = CustomerAgent()
    response = customer_agent.handle_query(state["user_input"])
    state["agent_response"] = response
    state["logs"].append("CustomerAgent handled query")
    return state


def inventory_agent_node(state: AgenticState):
    """
    Handles inventory-related queries using InventoryAgent.
    """
    inventory_agent = InventoryAgent()
    response = inventory_agent.handle_query(state["user_input"])
    state["agent_response"] = response
    state["logs"].append("InventoryAgent handled query")
    return state


# ------------------ Graph Builder ------------------

def build_graph():
    """
    Constructs and returns the full LangGraph workflow.
    """
    graph = StateGraph(AgenticState)

    # Define nodes
    graph.add_node("router", router_node)
    graph.add_node("customer_agent", customer_agent_node)
    graph.add_node("inventory_agent", inventory_agent_node)

    # Set entry point
    graph.set_entry_point("router")

    # Conditional routing
    graph.add_conditional_edges(
        "router",
        lambda state: state["agent_type"],
        {
            "customer": "customer_agent",
            "inventory": "inventory_agent",
        },
    )

    # All agent nodes go to END
    graph.add_edge("customer_agent", END)
    graph.add_edge("inventory_agent", END)

    # Compile it
    return graph.compile()
