from pydantic import BaseModel,ConfigDict
from typing import Optional
from app.utils import password
    
class UserCreate(BaseModel):
    name: str
    email: str
    password:str
    phone: Optional[str] = None
    
class UserLoginRequest(BaseModel):
    email: str
    password: str
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)