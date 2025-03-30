import logging
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.models.seller import Seller
from src.models.books import Book
from src.configurations.settings import settings

# Настроим базовое логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем engine
__async_engine = create_async_engine(settings.database_url, echo=True)

async def create_db_and_tables():
    global __async_engine

    if __async_engine is None:
        raise ValueError("You must call global_init() before using this method")

    async with __async_engine.begin() as conn:
        # Логируем начало создания таблиц
        logger.info("Создаём таблицы продавцов...")
        await conn.run_sync(Seller.metadata.create_all)
        logger.info("Таблица продавцов создана!")

        logger.info("Создаём таблицы книг...")
        await conn.run_sync(Book.metadata.create_all)
        logger.info("Таблица книг создана!")

# Запуск с явным циклом событий
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db_and_tables())
    loop.close()
