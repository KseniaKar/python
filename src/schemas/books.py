from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from typing import List

__all__ = ["IncomingBook", "ReturnedBook", "ReturnedAllbooks", "BookUpdate"]

# Базовый класс "Книги"
class BaseBook(BaseModel):
    title: str
    author: str
    year: int
    seller_id: int


# Входная схема
class IncomingBook(BaseBook):
    pages: int = Field(default=150, alias="count_pages")

    @field_validator("year")
    @staticmethod
    def validate_year(val: int):
        if val < 2020:
            raise PydanticCustomError("Validation error", "Year is too old!")
        return val


# Ответная схема одной книги
class ReturnedBook(BaseBook):
    id: int
    pages: int

    model_config = {
        "from_attributes": True
    }


# Список книг
class ReturnedAllbooks(BaseModel):
    books: List[ReturnedBook]

    model_config = {
        "from_attributes": True
    }


# ✨ Схема для обновления книги (PUT)
class BookUpdate(BaseModel):
    title: str
    author: str
    year: int
    pages: int
    seller_id: int
