from sqlalchemy.orm import Session # @unresolvedImport
from typing import List
from app.repository.customer_repository import create_customer as repo_create_customer
from app.repository.customer_repository import get_customers as repo_get_customers, get_customer_by_phone,get_customer
from app.repository.customer_repository import add_purchase as repo_add_purchase, delete_customer as repo_delete_customer,get_customer_purchases
from app.repository.product_repository import get_by_id
from app.model.Customer import Customer
from app.model.Customer_Purchase import CustomerPurchase
from app.schema.CustomerSchema import CustomerCreate
from app.exception import ConflictError, NotFoundError
from app.repository import stock_repository


# ----------------- Customer Services -----------------

def create_customer(db: Session, user_id: int, customer_data: CustomerCreate) -> Customer:
    customer = get_customer_by_phone(db,user_id,customer_data.phone)
    
    print(customer)
    if customer:
        raise ConflictError("Customer")
    
    resp = repo_create_customer(db, user_id, customer_data)
    return resp

def get_customers(db: Session, user_id: int) -> List[Customer]:
    return repo_get_customers(db, user_id)

def delete_customer(customer_id: int, db:Session, user_id: int):
    customer = get_customer(db,user_id,customer_id)
    
    if not customer:
        raise NotFoundError("Customer")
    
    return repo_delete_customer(db,customer)


def add_purchase(db: Session, user_id: int, customer_id: int, product_id: int, quantity: int, paid:int) -> CustomerPurchase:
    customer = get_customer(db,user_id,customer_id)
    
    print(customer)
    
    if not customer:
        raise NotFoundError("Customer")
    
    product = get_by_id(db,product_id,user_id)
    
    if not product:
        raise NotFoundError("Product")
    
    totalPrice = product.price * quantity
    pendingAmount = customer.pending
    pendingAmount = pendingAmount + totalPrice - paid
    customer.pending = pendingAmount
    
    added = repo_add_purchase(db, user_id, customer_id, product_id, quantity,paid)
    
    stock_repository.remove_stock(db,product_id,user_id,quantity,f'{customer.name} purchased {quantity} {product.unit} of {product.name}')
    return added

def customer_purchases(db: Session, user_id:int):
    customer_purchases = get_customer_purchases(db,user_id)
    
    return customer_purchases
