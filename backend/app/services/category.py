from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repositories.category import CategoryRepository
from ..schemas.category import CategoryCreate, CategoryResponse


class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_category_all(self) -> list[CategoryResponse]:
        categories = self.repository.get_all()
        response = [CategoryResponse.model_validate(cat) for cat in categories]
        return response

    def get_category_by_id(self, cat_id: int) -> CategoryResponse:
        category = self.repository.get_by_id(cat_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        response = CategoryResponse.model_validate(category)
        return response

    def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        category = self.repository.create(category_data)

        response = CategoryResponse.model_validate(category)
        return response
