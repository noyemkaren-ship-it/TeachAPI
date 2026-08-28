from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

engine = create_engine("sqlite:///db.sqlite")
Base = declarative_base()
session = scoped_session(sessionmaker(bind=engine))