from sqlalchemy import Column, Integer, String

from data.base import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    file_name = Column(String, nullable=False)
    grade = Column(Integer)