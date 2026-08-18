from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.auth.schemas import UserCreate
from app.auth.security import hash_password, verify_password
from fastapi import HTTPException

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def register_user(db: AsyncSession, user_in: UserCreate):
    existing_user = await get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        is_admin=False
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, user_in: UserCreate):
    db_user = await get_user_by_email(db, user_in.email)
    if not db_user or not verify_password(user_in.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return db_user