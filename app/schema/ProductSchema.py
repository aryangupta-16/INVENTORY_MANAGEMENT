from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Milk")
    category: Optional[str] = Field(None, min_length=2, max_length=50, example="Dairy")
    price: float = Field(..., gt=0, le=1_000_000, example=45.5)
    unit: str = Field(..., min_length=1, max_length=20, example="litre")
    stock: Optional[int] = Field(0, ge=0)
    threshold: Optional[int] = Field(5, ge=0)

    # @field_validator("name")
    # def strip_name(cls, v: str) -> str:
    #     return v.strip()

    # @field_validator("category")
    # def strip_category(cls, v: Optional[str]) -> Optional[str]:
    #     return v.strip() if v else v

    # @field_validator("threshold")
    # def validate_threshold(cls, v: Optional[int], info):
    #     stock = info.data.get("stock")
    #     if v is not None and stock is not None and v > stock:
    #         raise ValueError("Threshold cannot be greater than current stock")
    #     return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    price: Optional[float] = Field(None, gt=0, le=1_000_000)
    unit: Optional[str] = Field(None, min_length=1, max_length=20)
    stock: Optional[int] = Field(None, ge=0)
    threshold: Optional[int] = Field(None, ge=0)

    # @field_validator("name")
    # def strip_name(cls, v: Optional[str]) -> Optional[str]:
    #     return v.strip() if v else v

    # @field_validator("category")
    # def strip_category(cls, v: Optional[str]) -> Optional[str]:
    #     return v.strip() if v else v

    # @field_validator("threshold")
    # def validate_threshold(cls, v: Optional[int], info):
    #     stock = info.data.get("stock")
    #     if v is not None and stock is not None and v > stock:
    #         raise ValueError("Threshold cannot be greater than current stock")
    #     return v


class ProductOut(ProductBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
