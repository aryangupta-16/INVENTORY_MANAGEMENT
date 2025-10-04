from fastapi import APIRouter, Depends, HTTPException
from app.service import stock_service as StockService
from sqlalchemy.orm import Session # @UnresolvedImport
from app.schema.StockSchema import StockChange, StockChangeResponse
from app.config.database import get_db
from app.utils.security import get_current_user
from app.model.Product import Product
from typing import List

router = APIRouter(prefix="/stock", tags=["stock"])
@router.post("/add", response_model=StockChangeResponse)
def add_stock(payload: StockChange, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    movement = StockService.add_stock(db, payload.product_id, user.id, payload.change, payload.reason)
    if not movement:
        raise HTTPException(status_code=404, detail="Product not found")
    return movement

@router.post("/remove", response_model=StockChangeResponse)
def remove_stock(payload: StockChange, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    movement = StockService.remove_stock(db, payload.product_id, user.id, payload.change, payload.reason)
    if not movement:
        raise HTTPException(status_code=400, detail="Insufficient stock or product not found")
    return movement

@router.get("/{product_id}/history", response_model=List[StockChangeResponse])
def stock_history(product_id: int, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return StockService.history(db, product_id, user.id)

@router.get("/low")
def low_stock(db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return StockService.low_stock(db, user.id)