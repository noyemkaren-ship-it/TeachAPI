from typing import Union, List, Optional
from models import Book
from data.base import session
from sqlalchemy.exc import SQLAlchemyError
from schemas import BookCreate, BookUpdate


class BookRepository:
    def __init__(self):
        self.session = session

    def get_book_by_name(self, name: str) -> Optional[Book]:
        return self.session.query(Book).filter_by(name=name).first()

    def get_all_books(self) -> List[Book]:
        return self.session.query(Book).all()

    def create_book(self, book_data: BookCreate) -> Union[Book, dict]:
        try:
            book = Book(**book_data.model_dump())
            self.session.add(book)
            self.session.commit()
            self.session.refresh(book)
            return book
        except SQLAlchemyError as e:
            self.session.rollback()
            return {"Message": f"Book is not created: {str(e)}"}

    def delete_book_by_name(self, name: str) -> dict:
        try:
            book = self.get_book_by_name(name)
            if book is None:
                return {"Message": "Book not found"}

            self.session.delete(book)
            self.session.commit()
            return {"Message": f"Book '{name}' deleted successfully"}
        except SQLAlchemyError as e:
            self.session.rollback()
            return {"Message": f"Book is not deleted: {str(e)}"}

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        return self.session.query(Book).filter_by(id=book_id).first()

    def update_book(self, book_id: int, book_data: BookUpdate) -> Union[Book, dict]:
        try:
            existing_book = self.get_book_by_id(book_id)
            if existing_book is None:
                return {"Message": "Book not found"}

            # Обновляем только переданные поля
            update_data = book_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(existing_book, key, value)

            self.session.commit()
            self.session.refresh(existing_book)
            return existing_book
        except SQLAlchemyError as e:
            self.session.rollback()
            return {"Message": f"Book is not updated: {str(e)}"}