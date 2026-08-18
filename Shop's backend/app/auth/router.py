from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth import crud, schemas
from app.auth.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UserResponse)
async def register(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.register_user(db, user_in)

@router.post("/login", response_model=schemas.TokenResponse)
async def login(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud.auth_user(db, user_in)
    token = create_access_token(data={"sub": str(user.id), "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer"}
