from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.security import get_current_user
from app.auth.models import User
from app.cart import crud, schemas

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=schemas.CartResponse)
async def read_cart(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud.get_user_cart(db, current_user.id)

@router.post("/", response_model=schemas.CartItemResponse)
async def add_item(item_in: schemas.CartItemCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud.add_2_cart(db, current_user.id, item_in)

@router.delete("/{cart_item_id}")
async def delete_item(cart_item_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud.remove_cart(db, current_user.id, cart_item_id)