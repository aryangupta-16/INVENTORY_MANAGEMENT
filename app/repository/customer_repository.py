from sqlalchemy.orm import Session, joinedload # @unresolvedImport
from app.model.Customer_Purchase import CustomerPurchase
from app.model.Product import Product
from app.model.Customer import Customer
from app.model.Stock import Stock
from app.schema.CustomerSchema import CustomerCreate
from app.service import ai_service


# ----------------- Customer Functions -----------------

def create_customer(db: Session, user_id: int, customer_data: CustomerCreate):
    customer = Customer(**customer_data.dict(), user_id=user_id)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer: Customer):
    db.delete(customer)
    db.commit()
    return customer
    

def get_customers(db: Session, user_id: int):
    return db.query(Customer).filter(Customer.user_id == user_id).all()

def get_customer(db: Session, user_id: int, customer_id:int):
    return db.query(Customer).filter(Customer.user_id == user_id, Customer.id == customer_id).first()

def get_customer_by_phone(db:Session, user_id:int, phone: str):
    return db.query(Customer).filter(Customer.user_id == user_id, Customer.phone == phone).first()

def add_purchase(db: Session, user_id: int, customer_id: int, product_id: int, quantity: int):
    
    customer = db.query(Customer).filter(Customer.id == customer_id, Customer.user_id == user_id).first()
    if not customer:
        return None

    # Check product and stock
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    if not product or product.stock < quantity:
        return None
    

    ai_service.update_customer_vector(db, customer)
    
    product.stock -= quantity
    total_price = product.price * quantity

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


# def get_customer_purchases(db:Session,user_id:int):
#     customers = db.query(Customer).filter(Customer.user_id == user_id).all()
    
def get_customer_purchases(db: Session, user_id: int):
    # Fetch customers with their purchases and products in one go
    # customers = (
    #     db.query(Customer)
    #     .options(
    #         joinedload(Customer.purchases).joinedload(CustomerPurchase.product)
    #     )
    #     .filter(Customer.user_id == user_id)
    #     .all()
    # )
    
    purchases = (
        db.query(CustomerPurchase)
        .join(Customer, Customer.id == CustomerPurchase.customer_id)
        .join(Product, Product.id == CustomerPurchase.product_id)
        .options(
            joinedload(CustomerPurchase.customer),
            joinedload(CustomerPurchase.product)
        )
        .filter(Customer.user_id == user_id)
        .all()
    )

    # print(customers)
    result = []
    for purchase in purchases:
        result.append({
            "id": purchase.id,
            "customerId": purchase.customer.id,
            "customerName": purchase.customer.name,
            "productId": purchase.product.id if purchase.product else None,
            "productName": purchase.product.name if purchase.product else None,
            "quantity": purchase.quantity,
            "totalPrice": purchase.quantity * purchase.product.price if purchase.product else None,
            "date": purchase.created_at.isoformat() if hasattr(purchase, "created_at") else None
        })

    return result