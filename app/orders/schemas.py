from datetime import datetime
from pydantic import BaseModel
from app.products.schemas import ProductResponse

class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    price_at_purchase: float
    product: ProductResponse | None

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    created_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True