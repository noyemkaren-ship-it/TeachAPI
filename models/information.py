from data.base import Base
from sqlalchemy import Column, Integer, String

class Information(Base):
    __tablename__ = "information"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)
    subject = Column(String)