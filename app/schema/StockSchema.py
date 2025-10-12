from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class StockChange(BaseModel):
    product_id: int = Field(..., gt=0, description="ID of the product")
    change: int = Field(..., ne=0, description="Positive for add, negative for remove")
    reason: Optional[str] = Field(None, max_length=255, description="Reason for stock change")


class StockChangeResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    change: int
    reason: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
