# app/routes/product_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session # @UnresolvedImport
from typing import List, Optional

from app.schema.ProductSchema import ProductCreate, ProductOut, ProductUpdate
from app.service import product_service as ProductService
from app.config.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductOut, status_code=201)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    user: int = Depends(get_current_user),
):
    return ProductService.create_product(db, payload, user.id)

@router.get("/", response_model=List[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 50,
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None, alias="price_min"),
    price_max: Optional[float] = Query(None, alias="price_max"),
    db: Session = Depends(get_db),
    user: int = Depends(get_current_user),
):
    return ProductService.list_products(db, user.id, skip, limit, name, category, price_min, price_max)

@router.get("/low", response_model=List[ProductOut])
def low_stock(db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return ProductService.get_low_stock(db, user.id)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    p = ProductService.get_product(db, product_id, user.id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    updated = ProductService.update_product(db, product_id, payload, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found or not owned by vendor")
    return updated

@router.delete("/{product_id}", status_code=200)
def delete_product(product_id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    deleted = ProductService.delete_product(db, product_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found or not owned by vendor")
    return {"message": "Product deleted successfully"}
