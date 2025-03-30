from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.books import Book
from src.models.seller import Seller
from src.schemas.books import IncomingBook, ReturnedBook, ReturnedAllbooks, BookUpdate
from src.configurations import get_async_session

books_router = APIRouter(tags=["books"], prefix="/books")

# Создание книги
@books_router.post("/", response_model=ReturnedBook, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: IncomingBook,
    session: AsyncSession = Depends(get_async_session)
):
    seller = await session.get(Seller, book.seller_id)
    if not seller:
        raise HTTPException(status_code=400, detail="Seller not found")
    
    new_book = Book(**book.model_dump())

    session.add(new_book)
    await session.flush()
    return new_book

# Получение всех книг
@books_router.get("/", response_model=ReturnedAllbooks)
async def get_all_books(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Book))
    books = result.scalars().all()
    return {"books": books}

# Получение книги по ID
@books_router.get("/{book_id}", response_model=ReturnedBook)
async def get_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Удаление книги
@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await session.delete(book)
    await session.flush()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Обновление книги
@books_router.put("/{book_id}", response_model=ReturnedBook)
async def update_book(
    book_id: int,
    new_book_data: BookUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in new_book_data.model_dump(exclude_unset=True).items():

        setattr(book, key, value)

    await session.flush()
    return book
