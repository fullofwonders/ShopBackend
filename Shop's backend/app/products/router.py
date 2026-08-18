from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.products import crud, schemas
from app.auth.security import get_current_admin_user
from app.auth.models import User

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[schemas.ProductResponse])
async def read_products(db: AsyncSession = Depends(get_db)):
    return await crud.get_products(db)

@router.get("/{product_id}", response_model=schemas.ProductResponse)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schemas.ProductResponse)
async def create_product(
    product: schemas.ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user) # Только для админов
):
    return await crud.create_product(db, product)

@router.patch("/{product_id}", response_model=schemas.ProductResponse)
async def update_product(
    product_id: int,
    product_in: schemas.ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    return await crud.update_product(db, product_id, product_in)

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    return await crud.delete_product(db, product_id)