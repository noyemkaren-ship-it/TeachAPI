from models import *
from data.base import Base, engine

Base.metadata.create_all(engine)