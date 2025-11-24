from app.schema.ProductSchema import ProductCreate, ProductUpdate, ProductOut
from app.repository import product_repository
from sqlalchemy.orm import Session # @UnresolvedImport
from typing import List, Optional
from app.model.Product import Product
from app.exception import ConflictError, NotFoundError
from app.repository import stock_repository

def create_product(db: Session, product_in: ProductCreate, user_id: int) -> Product:
        product = product_repository.get_product_by_name(db,product_in.name,user_id)
        if product:
            raise ConflictError("Product")
        
        prod = product_repository.create_product(db, product_in, user_id)
        stock_repository.add_stock(db,prod.id,user_id,prod.stock)
        return prod

def get_product(db: Session, product_id: int, user_id: int) -> Optional[Product]:
    
        product = product_repository.get_by_id(db, product_id, user_id)
        if not product:
            raise NotFoundError("Product")

def list_products(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        name: Optional[str] = None,
        category: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
    ) -> List[Product]:
        return product_repository.list(db, user_id, skip, limit, name, category, price_min, price_max)

def update_product(db: Session, product_id: int, updates: ProductUpdate, user_id: int) -> Optional[Product]:
        prod = product_repository.get_by_id(db, product_id, user_id)
        if not prod:
            raise NotFoundError("Product")
        return product_repository.update(db, prod, updates)

def delete_product(db: Session, product_id: int, user_id: int) -> Optional[Product]:
        prod = product_repository.get_by_id(db, product_id, user_id)
        if not prod:
            raise NotFoundError("Product")
        return product_repository.delete(db, prod)

def get_low_stock(db: Session, user_id: int) -> List[Product]:
        return product_repository.low_stock(db, user_id)