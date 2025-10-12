from agents import Agent, handoff # @unresolvedImports
from .forecasting_agent import forecasting_agent
from .analytics_agent import analysis_agent
from dotenv import load_dotenv
load_dotenv()
import os



orchestrator_agent = Agent(
    name="InventoryOrchestrator",
    instructions=("""
You are a top-level inventory management assistant.  
Given a user query, use the available tools to understand context and decide whether this is a forecasting request (predict stockout, reorder) or an analytics request (detect slow movers).  
You have two tools: `search_vector_context` (to get related knowledge) and `fetch_sales_and_stock`.  
If the user is asking about “forecast”, “predict”, “when will it run out”, route to the forecasting_agent.  
If about “slow”, “stuck”, “unsold”, route to analytics_agent.  
Use context from vector store to assist your decision.
"""),
    model="gpt-5-nano",
    # tools=[search_vector_context, fetch_sales_and_stock],
    handoffs=[forecasting_agent,analysis_agent],
)
