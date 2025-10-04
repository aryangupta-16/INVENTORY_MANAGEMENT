from sqlalchemy.orm import Session # @unresolvedImport
from typing import List
from app.repository.customer_repository import create_customer as repo_create_customer
from app.repository.customer_repository import get_customers as repo_get_customers
from app.repository.customer_repository import add_purchase as repo_add_purchase
from app.model.Customer import Customer
from app.model.Customer_Purchase import CustomerPurchase
from app.schema.CustomerSchema import CustomerCreate

# ----------------- Customer Services -----------------

def create_customer(db: Session, user_id: int, customer_data: CustomerCreate) -> Customer:
    print("customer servicee")
    resp = repo_create_customer(db, user_id, customer_data)
    
    print(resp.phone)
    return resp

def get_customers(db: Session, user_id: int) -> List[Customer]:
    return repo_get_customers(db, user_id)

# ----------------- Customer Purchase Services -----------------

def add_purchase(db: Session, user_id: int, customer_id: int, product_id: int, quantity: int) -> CustomerPurchase:
    return repo_add_purchase(db, user_id, customer_id, product_id, quantity)
