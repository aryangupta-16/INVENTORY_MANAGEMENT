from sqlalchemy.orm import Session # @UnresolvedImport
from typing import List, Optional
from app.model.Product import Product
from app.schema.ProductSchema import ProductCreate, ProductUpdate


def create_product(db:Session,product_in: ProductCreate, user_id: int):
    db_product = Product(**product_in.model_dump(), user_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_by_id(db: Session, product_id: int, user_id: int):
    return db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()

def list(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        name: Optional[str] = None,
        category: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
    ) -> List[Product]:
        q = db.query(Product).filter(Product.user_id == user_id)
        if name:
            q = q.filter(Product.name.ilike(f"%{name}%")) # @UndefinedVariable
        if category:
            q = q.filter(Product.category == category)
        if price_min is not None:
            q = q.filter(Product.price >= price_min)
        if price_max is not None:
            q = q.filter(Product.price <= price_max)
        return q.offset(skip).limit(limit).all()
    
def update(db: Session, product: Product, updates: ProductUpdate) -> Product:
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(product, key, value)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

def delete(db: Session, product: Product) -> Product:
        db.delete(product)
        db.commit()
        return product
    
def low_stock(db: Session, vendor_id: int) -> List[Product]:
        return db.query(Product).filter(Product.user_id == vendor_id, Product.stock < Product.threshold).all()