from typing import List, Dict
from app.repository.ai_vector_db import query_vectors
from app.utils.embeddings import get_embedding

# -------- ANALYSIS TOOLS -------- #

def analyze_best_selling_products(limit: int = 5) -> List[Dict]:
    """
    Retrieves top-selling products from vector DB.
    """
    results = query_vectors(get_embedding("top selling products by quantity and revenue"))
    sorted_data = sorted(results, key=lambda x: x.get("quantity", 0), reverse=True)
    return sorted_data[:limit]


def analyze_customer_revenue() -> List[Dict]:
    """
    Retrieves customers ranked by total revenue contribution.
    """
    results = query_vectors(get_embedding("customer purchase revenue data"))
    sorted_customers = sorted(results, key=lambda x: x.get("total_revenue", 0), reverse=True)
    return sorted_customers


def compare_sales_periods(period1: str, period2: str) -> Dict:
    """
    Compares sales performance between two time periods.
    """
    data1 = query_vectors(get_embedding(f"sales data for {period1}"))
    data2 = query_vectors(get_embedding(f"sales data for {period2}"))

    total1 = sum(item.get("revenue", 0) for item in data1)
    total2 = sum(item.get("revenue", 0) for item in data2)

    return {
        "period1": period1,
        "period2": period2,
        "difference": round(total2 - total1, 2),
        "percentage_change": round(((total2 - total1) / total1) * 100, 2) if total1 else None
    }

