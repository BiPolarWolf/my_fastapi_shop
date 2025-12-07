from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.category import CategoryResponse
from ..services.category import CategoryService

router = APIRouter(prefix="/api/categories/", tags=["categories"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_category_all()


@router.get(
    "{category_id}/", response_model=CategoryResponse, status_code=status.HTTP_200_OK
)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_category_by_id(category_id)
