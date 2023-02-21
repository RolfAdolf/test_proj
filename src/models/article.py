from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'), index=True)
    category = relationship('Category', backref='categories')
