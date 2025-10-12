from agents import Agent, function_tool # @unresolvedImport
from typing import Dict, Any
from app.tools.analysis_tools import (
    analyze_best_selling_products,
    analyze_customer_revenue,
    compare_sales_periods
) # @unresolvedImport
from dotenv import load_dotenv
load_dotenv()

# Wrap tools
@function_tool
def best_selling_products_tool(limit: int = 5) -> Dict[str, Any]:
    return {"top_products": analyze_best_selling_products(limit)}

@function_tool
def customer_revenue_tool() -> Dict[str, Any]:
    return {"customer_revenue": analyze_customer_revenue()}

@function_tool
def compare_sales_tool(period1: str, period2: str) -> Dict[str, Any]:
    return compare_sales_periods(period1, period2)

# Create AnalysisAgent
analysis_agent = Agent(
    name="AnalysisAgent",
    instructions=("You are an agent that performs sales and customer analytics, compares sales between periods, and identifies top-performing products and customers."),
    model="gpt-5-nano",
    tools=[best_selling_products_tool, customer_revenue_tool, compare_sales_tool]
)

# Wrapper to call agent
def handle_analysis(query: str):
    return analysis_agent.run(query)
