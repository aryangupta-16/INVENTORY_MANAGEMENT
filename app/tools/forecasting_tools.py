from typing import Dict, List
from datetime import datetime
from app.repository.ai_vector_db import query_vectors
from app.utils.embeddings import get_embedding

# -------- FORECASTING TOOLS -------- #

def forecast_product_demand(product_name: str, weeks_ahead: int = 4) -> Dict:
    """
    Predicts future product demand by analyzing similar entries in vector DB.
    """
    results = query_vectors([float(x) for x in get_embedding(f"sales history for {product_name}")])
    print(results)
    if not results:
        return {"error": f"No sales data found for {product_name}"}

    total_sales = sum(item.get("stock", 0) for item in results)
    avg_weekly_sales = total_sales / len(results) if results else 0

    return {
        "product": product_name,
        "weeks_ahead": weeks_ahead,
        "predicted_sales": round(avg_weekly_sales * weeks_ahead, 2),
        "generated_at": datetime.utcnow().isoformat()
    }


def forecast_total_revenue(weeks_ahead: int = 4) -> Dict:
    """
    Predicts total revenue for future weeks using average past revenue.
    """
    results = query_vectors([float(x) for x in get_embedding("total sales revenue history")])
    if not results:
        return {"error": "No revenue data found"}

    total_revenue = sum(item.get("revenue", 0) for item in results)
    avg_weekly_revenue = total_revenue / len(results) if results else 0

    return {
        "weeks_ahead": weeks_ahead,
        "predicted_revenue": round(avg_weekly_revenue * weeks_ahead, 2),
        "generated_at": datetime.utcnow().isoformat()
    }


def forecast_low_stock_products(threshold: int = 10) -> List[Dict]:
    """
    Detects products that might soon run low on stock.
    """
    results = query_vectors([float(x) for x in get_embedding("product stock levels and sales velocity")])
    return [item for item in results if item.get("predicted_stock", 0) < threshold]


