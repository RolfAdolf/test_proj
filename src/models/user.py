from sqlalchemy import Column, Integer, String
from src.models.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
