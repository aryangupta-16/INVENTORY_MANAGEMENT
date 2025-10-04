from sqlalchemy.orm import Session # @unresolvedImport
from app.model.Customer_Purchase import CustomerPurchase
from app.model.Product import Product
from app.model.Customer import Customer
from app.schema.CustomerSchema import CustomerCreate

# ----------------- Customer Functions -----------------

def create_customer(db: Session, user_id: int, customer_data: CustomerCreate):
    customer = Customer(**customer_data.dict(), user_id=user_id)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_customers(db: Session, user_id: int):
    return db.query(Customer).filter(Customer.user_id == user_id).all()

# ----------------- Customer Purchase Functions -----------------

def add_purchase(db: Session, user_id: int, customer_id: int, product_id: int, quantity: int):
    # Ensure customer belongs to this user
    customer = db.query(Customer).filter(Customer.id == customer_id, Customer.user_id == user_id).first()
    if not customer:
        return None

    # Check product and stock
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    if not product or product.stock < quantity:
        return None

    # Deduct stock
    product.stock -= quantity
    total_price = product.price * quantity

    # Create purchase record
    purchase = CustomerPurchase(
        customer_id=customer_id,
        product_id=product_id,
        quantity=quantity,
        price=total_price
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase
