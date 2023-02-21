from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.category import Category
from src.models.schemas.category.category_request import CategoryRequest


class CategoriesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Category]:
        categories = (
            self.session
            .query(Category)
            .order_by(
                Category.id.desc()
            )
            .all()
        )
        return categories

    def get(self, category_id: int) -> Category:
        category = (
            self.session
            .query(Category)
            .filter(
                Category.id == category_id
            )
            .first()
        )
        return category

    def add(self, category_schema: CategoryRequest) -> Category:
        category = Category(**category_schema.dict())
        self.session.add(category)
        self.session.commit()
        return category

    def update(self, category_id: int, category_schema: CategoryRequest) -> Category:
        category = self.get(category_id)
        for field, value in category_schema:
            setattr(category, field, value)
        self.session.commit()
        return category

    def delete(self, category_id: int):
        category = self.get(category_id)
        self.session.delete(category)
        self.session.commit()
