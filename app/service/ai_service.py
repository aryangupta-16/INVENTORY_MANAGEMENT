# app/services/ai_service.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session   # @unresolvedImport
from app.utils.embeddings import get_embedding
from app.repository import ai_repo
# from app.model import Product, Customer, Customer_Purchase as CustomerPurchase  # your existing models
from app.model.Customer import Customer
from app.model.Customer_Purchase import CustomerPurchase
from app.model.Product import Product

def compute_product_summary(db: Session, product: Product):
    sold_30d = db.query(CustomerPurchase).filter(
        CustomerPurchase.product_id == product.id,
        CustomerPurchase.created_at >= datetime.utcnow() - timedelta(days=30)
    ).count()
    summary = f"{product.name}, Category: {product.category}, Stock: {product.stock}, Sold last 30d: {sold_30d}"
    metadata = {
        "product_id": product.id,
        "user_id": product.user_id,
        "name": product.name,
        "category": product.category,
        "stock": product.stock,
        "sold_last_30d": sold_30d,
    }
    return summary, metadata

def compute_customer_summary(db: Session, customer: Customer):
    purchases_90d = db.query(CustomerPurchase).filter(
        CustomerPurchase.customer_id == customer.id,
        CustomerPurchase.created_at >= datetime.utcnow() - timedelta(days=90)
    ).all()
    total_purchases = len(purchases_90d)
    last_purchase_date = max([p.created_at for p in purchases_90d], default=None)
    product_counts = {}
    for p in purchases_90d:
        product = db.query(Product).filter(Product.id == p.product_id).first()
        if product:
            product_counts[product.name] = product_counts.get(product.name, 0) + 1
    frequent_products = sorted(product_counts, key=product_counts.get, reverse=True)[:5]

    summary = f"{customer.name}, Total purchases last 90d: {total_purchases}, Last purchase: {last_purchase_date}, Frequent products: {', '.join(frequent_products)}"
    metadata = {
        "customer_id": customer.id,
        "user_id": customer.user_id,
        "name": customer.name,
        "total_purchases_last_90d": total_purchases,
        "last_purchase_date": last_purchase_date,
        "frequent_products": frequent_products
    }
    return summary, metadata

def update_product_vector(db: Session, product: Product):
    summary, metadata = compute_product_summary(db, product)
    vector = get_embedding(summary)
    entry_id = product.user_id * 100000 + product.id
    ai_repo.upsert_product_vector(entry_id, vector, metadata)

def update_customer_vector(db: Session, customer: Customer):
    summary, metadata = compute_customer_summary(db, customer)
    vector = get_embedding(summary)
    entry_id = customer.user_id * 100000 + customer.id
    ai_repo.upsert_customer_vector(entry_id, vector, metadata)

def handle_ai_query(user_id: int, query: str):
    query_vector = get_embedding(query)
    results = ai_repo.query_vectors(query_vector, top_k=5)
    results = [r for r in results if r.get('user_id') == user_id]

    print(results)
    if not results:
        answer = "No relevant data found."
    else:
        answer_lines = []
        for r in results:
            if 'product_id' in r:
                answer_lines.append(f"Product {r['name']} has {r['stock']} units in stock.")
            elif 'customer_id' in r:
                answer_lines.append(f"Customer {r['name']} purchased {r['total_purchases_last_90d']} times.")
        answer = "\n".join(answer_lines)

    return {"answer": answer, "related_entries": results}
