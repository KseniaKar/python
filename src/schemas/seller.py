from pydantic import BaseModel, EmailStr
from typing import List, Optional
from src.schemas.books import ReturnedBook


# Схема для создания продавца
class SellerCreate(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr
    password: str


# Схема для отображения продавца (без пароля)
class SellerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    e_mail: EmailStr

    model_config = {
        "from_attributes": True
    }


# Схема для отображения продавца с книгами
class SellerWithBooks(SellerResponse):
    books: List[ReturnedBook] = []

    model_config = {
        "from_attributes": True
    }


# Схема для обновления продавца (без пароля и книг)
class SellerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    e_mail: Optional[EmailStr] = None
