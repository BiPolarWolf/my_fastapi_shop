from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> List[Category]:
        return self.db.query(Category).all()

    def get_by_id(self, cat_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == cat_id).first()

    def get_by_slug(self, cat_slug: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.slug == cat_slug).first()

    def create(self, cat_data: CategoryCreate):
        new_category = Category(**cat_data.model_dump())
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category
