from app.repository import stock_repository
from sqlalchemy.orm import Session # @UnresolvedImport
from typing import List
from app.model import Product, Stock

def add_stock(db: Session, product_id: int, user_id: int, quantity: int, reason: str = None) -> Stock:
        return stock_repository.add_stock(db, product_id, user_id, quantity, reason)

    
def remove_stock(db: Session, product_id: int, user_id: int, quantity: int, reason: str = None) -> Stock:
        return stock_repository.remove_stock(db, product_id, user_id, quantity, reason)

    
def history(db: Session, product_id: int, user_id: int) -> List[Stock]:
        return stock_repository.history(db, product_id, user_id)

    
def low_stock(db: Session, user_id: int) -> List[Product]:
        return stock_repository.low_stock(db, user_id)