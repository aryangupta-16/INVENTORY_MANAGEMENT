from typing import List, Dict

def get_sales_timeseries(user_id: str, product_ids: List[str], days: int = 30) -> Dict[str, List[int]]:
    """
    Returns a dict: product_id → list of daily sales (last `days` days).
    """
    # MOCK: return random or static data
    return {pid: [5, 4, 6, 7, 3, 5, 5] for pid in product_ids}

def get_current_stock(user_id: str, product_ids: List[str]) -> Dict[str, int]:
    """
    product_id → current stock.
    """
    # MOCK: static values
    return {pid: 50 for pid in product_ids}
