from pydantic import BaseModel, ConfigDict
from typing import List,Optional
from sqlalchemy.orm import Session # @UnresolvedImport  
from pydantic.config import ConfigDict
from datetime import datetime

class StockChange(BaseModel):
    
    product_id: int
    change: int
    reason: Optional[str] = None
    
class StockChangeResponse(BaseModel):
    
    id: int
    product_id: int
    user_id: int
    change: int
    reason: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)