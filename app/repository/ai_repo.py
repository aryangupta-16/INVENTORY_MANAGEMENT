# app/repositories/ai_repo.py
from app.repository import ai_vector_db

def upsert_product_vector(entry_id: int, vector: list, metadata: dict):
    ai_vector_db.upsert_vector(entry_id, vector, metadata)

def upsert_customer_vector(entry_id: int, vector: list, metadata: dict):
    ai_vector_db.upsert_vector(entry_id, vector, metadata)

def query_vectors(vector: list, top_k: int = 5):
    return ai_vector_db.query_vectors(vector, top_k)
