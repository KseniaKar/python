from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.seller import Seller
from src.models.books import Book
from src.schemas.seller import SellerCreate, SellerResponse, SellerUpdate, SellerWithBooks
from src.configurations import get_async_session

from src.utils.security import hash_password
from sqlalchemy.orm import selectinload
from fastapi import Response

sellers_router = APIRouter(tags=["sellers"], prefix="/seller")

# Создание нового продавца

# Получение всех продавцов (можно с книгами)
@sellers_router.get("/", response_model=dict[str, list[SellerWithBooks]])
async def get_all_sellers(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Seller).options(selectinload(Seller.books))
    )
    sellers = result.scalars().all()
    return {"sellers": sellers}

    
@sellers_router.post("/", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
async def create_seller(seller_data: SellerCreate, session: AsyncSession = Depends(get_async_session)):
    hashed_password = hash_password(seller_data.password)
    new_seller = Seller(**seller_data.model_dump(exclude={"password"}), password=hashed_password)
    session.add(new_seller)
    await session.flush()
    return new_seller

# Получение продавца по ID, включая книги
@sellers_router.get("/{seller_id}", response_model=SellerWithBooks)
async def get_seller_with_books(
    seller_id: int = Path(..., title="ID продавца"),
    session: AsyncSession = Depends(get_async_session),
):
    query = (
        select(Seller)
        .options(selectinload(Seller.books))  # 👈 вот оно
        .where(Seller.id == seller_id)
    )
    result = await session.execute(query)
    seller = result.scalars().first()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    return seller

# Обновление данных продавца (без книг и пароля)
@sellers_router.put("/{seller_id}", response_model=SellerResponse)
async def update_seller(
    seller_id: int = Path(..., title="ID продавца"),
    seller_data: SellerUpdate = ...,
    session: AsyncSession = Depends(get_async_session)
):
    seller = await session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    for key, value in seller_data.model_dump(exclude_unset=True).items():

        setattr(seller, key, value)

    await session.flush()
    return seller

# Удаление продавца и всех его книг
@sellers_router.delete("/{seller_id}", status_code=204)
async def delete_seller(
    seller_id: int = Path(...),
    session: AsyncSession = Depends(get_async_session)
):
    seller = await session.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    await session.delete(seller)
    await session.flush()
    return Response(status_code=204)  
