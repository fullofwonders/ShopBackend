from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.orders.models import Order, OrderItem
from app.cart.models import CartItem
from fastapi import HTTPException


async def checkout_order(db: AsyncSession, user_id: int):
    cart_result = await db.execute(
        select(CartItem).where(CartItem.user_id == user_id).options(joinedload(CartItem.product))
    )
    cart_items = cart_result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0.0
    for item in cart_items:
        if item.product.quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough '{item.product.title}' in stock.")
        total_price += item.quantity * item.product.price

    db_order = Order(user_id=user_id, total_price=total_price)
    db.add(db_order)
    await db.flush()

    for item in cart_items:
        item.product.quantity -= item.quantity
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.product.price
        )
        db.add(db_order_item)
        await db.delete(item)

    await db.commit()

    result = await db.execute(
        select(Order).where(Order.id == db_order.id).options(joinedload(Order.items).joinedload(OrderItem.product))
    )
    return result.scalar_one()


async def get_user_orders(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Order).where(Order.user_id == user_id).options(joinedload(Order.items).joinedload(OrderItem.product))
    )
    return result.scalars().all()