from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.products.models import Product
from app.products.schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException


async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()


async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, product_id: int, product_update: ProductUpdate):
    db_product = await get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.model_dump(exclude_unset=True)

    if "title" in update_data:
        db_product.title = update_data["title"]
    if "description" in update_data:
        db_product.description = update_data["description"]
    if "price" in update_data:
        db_product.price = update_data["price"]
    if "quantity" in update_data:
        db_product.quantity = update_data["quantity"]
    if "category_id" in update_data:
        db_product.category_id = update_data["category_id"]

    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(db_product)
    await db.commit()
    return {"message": f"Product with id {product_id} deleted successfully"}