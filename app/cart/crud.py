from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.cart.models import CartItem
from app.cart.schemas import CartItemCreate
from app.products.models import Product
from fastapi import HTTPException


async def get_user_cart(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(CartItem).where(CartItem.user_id == user_id).options(joinedload(CartItem.product))
    )
    items = result.scalars().all()
    total_price = sum(item.quantity * item.product.price for item in items)
    return {"items": items, "total_price": total_price}


async def add_to_cart(db: AsyncSession, user_id: int, item_in: CartItemCreate):
    prod_result = await db.execute(select(Product).where(Product.id == item_in.product_id))
    if not prod_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")

    cart_result = await db.execute(
        select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == item_in.product_id)
    )
    existing_item = cart_result.scalar_one_or_none()

    if existing_item:
        existing_item.quantity += item_in.quantity
        db_item = existing_item
    else:
        db_item = CartItem(user_id=user_id, product_id=item_in.product_id, quantity=item_in.quantity)
        db.add(db_item)

    await db.commit()
    await db.refresh(db_item, ["product"])
    return db_item


async def remove_from_cart(db: AsyncSession, user_id: int, cart_item_id: int):
    result = await db.execute(
        select(CartItem).where(CartItem.id == cart_item_id, CartItem.user_id == user_id)
    )
    db_item = result.scalar_one_or_none()
    if not db_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await db.delete(db_item)
    await db.commit()
    return {"message": "Item removed from cart"}