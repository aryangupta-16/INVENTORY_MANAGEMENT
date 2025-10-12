from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, constr, field_validator, StringConstraints
import re

PhoneNumber = Annotated[str, StringConstraints(pattern=r'^\+?\d{10,15}$')]

class UserCreate(BaseModel):
    name: constr(strip_whitespace=True, min_length=2, max_length=50)
    email: EmailStr
    password: constr(min_length=4, max_length=36)
    phone: Optional[PhoneNumber] = None

    # @field_validator("password")
    # def validate_password_strength(cls, v: str) -> str:
    #     if not any(c.isupper() for c in v):
    #         raise ValueError("Password must contain at least one uppercase letter")
    #     if not any(c.islower() for c in v):
    #         raise ValueError("Password must contain at least one lowercase letter")
    #     if not any(c.isdigit() for c in v):
    #         raise ValueError("Password must contain at least one digit")
    #     if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for c in v):
    #         raise ValueError("Password must contain at least one special character")
    #     return v

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=4, max_length=36)

class UserUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=2, max_length=50)] = None
    email: Optional[EmailStr] = None
    phone: Optional[PhoneNumber] = None
    password: Optional[constr(min_length=4, max_length=36)] = None

    # @field_validator("password")
    # def validate_password_strength(cls, v: Optional[str]) -> Optional[str]:
    #     if v is None:
    #         return v
    #     if not any(c.isupper() for c in v):
    #         raise ValueError("Password must contain at least one uppercase letter")
    #     if not any(c.islower() for c in v):
    #         raise ValueError("Password must contain at least one lowercase letter")
    #     if not any(c.isdigit() for c in v):
    #         raise ValueError("Password must contain at least one digit")
    #     if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for c in v):
    #         raise ValueError("Password must contain at least one special character")
    #     return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
