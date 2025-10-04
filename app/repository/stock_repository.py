from app.model.Stock import Stock
from app.model.Product import Product
from sqlalchemy.orm import Session # @UnresolvedImport
from typing import List


def add_stock(db:Session, product_id:int, user_id:int, quantity: int, reason: str = None):
    db_product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    
    if not db_product:
        return None
    db_product.stock += quantity
    
    db_stock = Stock(product_id=product_id, user_id=user_id, change=quantity, reason=reason)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


def remove_stock(db:Session, product_id:int, user_id:int, quantity: int, reason: str = None):
    db_product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    
    if not db_product or db_product.stock < quantity:
        return None
    
    db_product.stock -= quantity
    
    db_stock = Stock(product_id=product_id, user_id=user_id, change=quantity, reason=reason)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def history(db:Session, product_id:int, user_id:int):
    return db.query(Stock).filter(Stock.product_id == product_id, Stock.user_id == user_id).order_by(Stock.created_at.desc()).all() #@UndefinedVariable

def low_stock(db: Session, user_id: int) -> List[Product]:
        return db.query(Product).filter(
            Product.user_id == user_id,
            Product.stock < Product.threshold
        ).all()