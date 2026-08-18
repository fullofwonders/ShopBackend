from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.security import get_current_user
from app.auth.models import User
from app.orders import crud, schemas

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/checkout", response_model=schemas.OrderResponse)
async def checkout(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud.checkout_order(db, current_user.id)

@router.get("/", response_model=list[schemas.OrderResponse])
async def get_my_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud.get_user_orders(db, current_user.id)