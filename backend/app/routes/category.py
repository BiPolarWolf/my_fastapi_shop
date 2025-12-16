from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryResponse
from app.services.category import CategoryService

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", status_code=status.HTTP_200_OK, response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_category_all()


@router.get(
    "/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK
)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_category_by_id(category_id)
