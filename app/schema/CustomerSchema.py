from pydantic import BaseModel, ConfigDict,field_serializer
from typing import Optional
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    
class CustomerOut(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    user_id: int
    
    @field_serializer("phone")
    def serialize_phone(self, value: int | str) -> str:
        return str(value)
    
    model_config = ConfigDict(from_attributes=True)

class CustomerPurchaseCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

class CustomerPurchaseOut(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    price: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)