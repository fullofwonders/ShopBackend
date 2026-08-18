from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.categories import crud, schemas

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[schemas.CategoryResponse])
async def read_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db)

@router.post("/", response_model=schemas.CategoryResponse)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(db, category)