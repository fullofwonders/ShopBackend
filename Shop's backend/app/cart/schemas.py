from pydantic import BaseModel, Field
from app.products.schemas import ProductResponse

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(1, gt=0)

class CartItemResponse(BaseModel):
    id: int
    quantity: int
    product: ProductResponse

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total_price: float