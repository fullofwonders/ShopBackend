from fastapi import FastAPI
from app.database import engine, Base

from app.products.models import Product
from app.categories.models import Category
from app.auth.models import User
from app.cart.models import CartItem
from app.orders.models import Order, OrderItem

from app.products.router import router as products_router
from app.categories.router import router as categories_router
from app.auth.router import router as auth_router
from app.cart.router import router as cart_router
from app.orders.router import router as orders_router

app = FastAPI(title="Shop's API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(products_router)
app.include_router(categories_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(orders_router)