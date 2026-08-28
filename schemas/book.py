from pydantic import BaseModel, ConfigDict
from typing import Optional


class BookBase(BaseModel):
    """Базовая схема книги"""
    name: str
    description: Optional[str] = None
    file_name: str
    grade: Optional[int] = None


class BookCreate(BookBase):
    """Схема для создания книги"""
    pass


class BookUpdate(BaseModel):
    """Схема для обновления книги"""
    name: Optional[str] = None
    description: Optional[str] = None
    file_name: Optional[str] = None
    grade: Optional[int] = None


class BookResponse(BookBase):
    """Схема для ответа с данными книги"""
    model_config = ConfigDict(from_attributes=True)

    id: int