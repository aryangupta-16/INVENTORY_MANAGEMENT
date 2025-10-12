from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session # @unresolvedImport
from typing import List
from app.config.database import get_db
from app.schema.CustomerSchema import CustomerCreate, CustomerOut, CustomerPurchaseCreate, CustomerPurchaseOut
from app.service.customer_service import create_customer, get_customers, add_purchase, delete_customer as customer_delete_customer,customer_purchases
from app.utils.security import get_current_user

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerOut)
def create_customer_endpoint(payload: CustomerCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    return create_customer(db, user.id, payload)

@router.get("/")
def list_customers_endpoint(db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    # print("idd",user.id)
    return get_customers(db, user.id)

@router.delete("/{customer_id}", status_code=200)
def delete_customer(customer_id,db:Session = Depends(get_db), user :int= Depends(get_current_user)):
    deleted = customer_delete_customer(customer_id,db,user.id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found or not owned by vendor")
    return {"message": "Customer deleted successfully"}

@router.post("/purchase", response_model=CustomerPurchaseOut)
def add_purchase_endpoint(payload: CustomerPurchaseCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    purchase = add_purchase(db, user.id, payload.customer_id, payload.product_id, payload.quantity)
    if not purchase:
        raise HTTPException(status_code=400, detail="Invalid customer/product or insufficient stock")
    return purchase

@router.get("/purchases")
def get_purchase_endpoint(db:Session = Depends(get_db), user:int = Depends(get_current_user)):
    return customer_purchases(db,user.id)