from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.categories.models import Category
from app.categories.schemas import CategoryCreate
from fastapi import HTTPException

async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()

async def create_category(db: AsyncSession, category: CategoryCreate):
    existing_category = await db.execute(select(Category).where(Category.name == category.name))
    if existing_category.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Category already exists")

    db_category = Category(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category