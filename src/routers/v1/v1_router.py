from fastapi import APIRouter
from src.routers.sellers import sellers_router  # Импортируем маршруты для продавцов
from src.routers.books import books_router  # Импортируем маршруты для книг

# Создаем основной роутер версии 1
v1_router = APIRouter(prefix="/api/v1")

# Регистрируем маршруты для продавцов и книг
v1_router.include_router(sellers_router)
v1_router.include_router(books_router)
