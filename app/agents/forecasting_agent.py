from agents import Agent, function_tool, ModelSettings # @unresolvedImport
from typing import Dict, Any
from app.tools.forecasting_tools import (
    forecast_product_demand,
    forecast_total_revenue,
    forecast_low_stock_products
)
from dotenv import load_dotenv
load_dotenv()

# Wrap each tool as a function_tool
@function_tool
def forecast_product_tool(product_name: str, weeks_ahead: int = 4) -> Dict[str, Any]:
    """
    Tool: forecast_product_tool
    Description: Predict future demand for a specific product using sales history.
    Use this tool whenever the query mentions product forecasts, sales predictions, or expected stock depletion.
    Input: product_name (str), weeks_ahead (int)
    Output: dict containing predicted sales and stock forecast.
    """
    return forecast_product_demand(product_name, weeks_ahead)

@function_tool
def forecast_revenue_tool(weeks_ahead: int = 4) -> Dict[str, Any]:
    """
    Tool: forecast_revenue_tool
    Description: Predict total revenue for upcoming weeks based on historical sales.
    Use this tool whenever the query mentions revenue forecast or total expected sales.
    Input: weeks_ahead (int)
    Output: dict containing projected revenue.
    """
    return forecast_total_revenue(weeks_ahead)

@function_tool
def forecast_low_stock_tool(threshold: int = 10) -> Dict[str, Any]:
    """
    Tool: forecast_low_stock_tool
    Description: Detect products that may run low on stock soon.
    Use this tool whenever the query mentions low stock, stock depletion, or reorder recommendations.
    Input: threshold (int)
    Output: dict containing products predicted to run low.
    """
    return {"low_stock_products": forecast_low_stock_products(threshold)}

# Create ForecastingAgent
forecasting_agent = Agent(
    name="ForecastingAgent",
    instructions=(
        "You are an agent that forecasts stock depletion, total revenue, "
        "and predicts low-stock products for vendors. "
        "You have access to following tools: "
        "forecast_product_tool, forecast_revenue_tool, forecast_low_stock_tool."
        "Always call the tool and assume few things if you have to but give the proper answer and don't ask question back"
    ),
    model="gpt-5-nano",
    tools=[forecast_product_tool, forecast_revenue_tool, forecast_low_stock_tool],
    model_settings=ModelSettings(tool_choice="forecast_product_tool")
)

# Wrapper to call agent
def handle_forecasting(query: str):
    return forecasting_agent.run(query)
