from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.product import ProductResponse, ProductResponseList
from ..services.product import ProductService

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_products_all()


@router.get(
    "/{product_id}/", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product_by_id(product_id)


@router.get(
    "/category/{category_id}/",
    response_model=ProductResponseList,
    status_code=status.HTTP_200_OK,
)
def get_product_by_category(category_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_products_by_category(category_id)
