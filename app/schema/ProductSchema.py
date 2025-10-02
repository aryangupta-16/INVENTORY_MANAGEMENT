from pydantic import BaseModel,ConfigDict, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., example="Milk")
    category: Optional[str] = Field(None, example="Dairy")
    price: float = Field(..., example=45.5)
    unit: str = Field(..., example="litre")
    stock: Optional[int] = Field(0, ge=0)
    threshold: Optional[int] = Field(5, ge=0)
    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    unit: Optional[str] = None
    stock: Optional[int] = None
    threshold: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)