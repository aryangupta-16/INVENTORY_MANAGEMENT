from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_serializer
from typing import Optional
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Customer full name")
    email: Optional[EmailStr] = Field(None, description="Valid email address")
    phone: Optional[str] = Field(
        None,
        pattern=r'^\+?\d{10,15}$',
        description="Phone number in E.164 format (+1234567890)"
    )


class CustomerOut(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    user_id: int

    @field_serializer("phone")
    def serialize_phone(self, value: Optional[str]) -> Optional[str]:
        return str(value) if value is not None else None

    model_config = ConfigDict(from_attributes=True)


class CustomerPurchaseCreate(BaseModel):
    customer_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, description="Quantity purchased must be positive")
    paid: int = Field(...,gt=0)


class CustomerPurchaseOut(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    price: float = Field(..., gt=0)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
