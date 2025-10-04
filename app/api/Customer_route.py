from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session # @unresolvedImport
from typing import List
from app.config.database import get_db
from app.schema.CustomerSchema import CustomerCreate, CustomerOut, CustomerPurchaseCreate, CustomerPurchaseOut
from app.service.customer_service import create_customer, get_customers, add_purchase
from app.utils.security import get_current_user

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerOut)
def create_customer_endpoint(payload: CustomerCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return create_customer(db, user.id, payload)

@router.get("/", response_model=List[CustomerOut])
def list_customers_endpoint(db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return get_customers(db, user.id)

@router.post("/purchase", response_model=CustomerPurchaseOut)
def add_purchase_endpoint(payload: CustomerPurchaseCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    purchase = add_purchase(db, user.id, payload.customer_id, payload.product_id, payload.quantity)
    if not purchase:
        raise HTTPException(status_code=400, detail="Invalid customer/product or insufficient stock")
    return purchase
