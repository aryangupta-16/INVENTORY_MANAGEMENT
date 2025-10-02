from app.schema.ProductSchema import ProductCreate, ProductUpdate, ProductOut
from app.repository import product_repository
from sqlalchemy.orm import Session # @UnresolvedImport
from typing import List, Optional
from fastapi import HTTPException, status
from app.model.Product import Product


def create_product(db: Session, product_in: ProductCreate, user_id: int) -> Product:
        return product_repository.create_product(db, product_in, user_id)

def get_product(db: Session, product_id: int, user_id: int) -> Optional[Product]:
        return product_repository.get_by_id(db, product_id, user_id)

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
            return None
        return product_repository.update(db, prod, updates)

def delete_product(db: Session, product_id: int, user_id: int) -> Optional[Product]:
        prod = product_repository.get_by_id(db, product_id, user_id)
        if not prod:
            return None
        return product_repository.delete(db, prod)

def get_low_stock(db: Session, user_id: int) -> List[Product]:
        return product_repository.low_stock(db, user_id)