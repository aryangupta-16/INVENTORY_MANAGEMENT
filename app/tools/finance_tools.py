# app/tools/finance_tools.py
from sqlalchemy.orm import Session
from app.repository.customer_repository import get_customer, add_purchase

def check_balance(db: Session, user_id: int, customer_id: int):
    customer = get_customer(db, user_id, customer_id)
    if not customer:
        return {"error": "Customer not found"}
    return {"customer": customer.name, "pending": customer.pending}

def record_payment(db: Session, user_id: int, customer_id: int, amount: int):
    customer = get_customer(db, user_id, customer_id)
    if not customer:
        return {"error": "Customer not found"}
    customer.pending -= amount
    if customer.pending < 0:
        customer.pending = 0
    db.commit()
    return {"customer": customer.name, "pending": customer.pending}
