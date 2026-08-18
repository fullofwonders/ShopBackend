from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True