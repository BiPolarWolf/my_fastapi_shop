from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from ..models.product import Product
from ..schemas.product import ProductCreate


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> List[Product]:
        return self.db.query(Product).options(joinedload(Product.category)).all()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
            .first()
        )

    def get_by_category(self, cat_id: int) -> List[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.category_id == cat_id)
            .all()
        )

    def get_by_ids(self, ids: List[int]) -> List[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id.in_(ids))
            .all()
        )

    def create(self, product_data: ProductCreate) -> Product:
        new_product = Product(**product_data.model_dump())

        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)

        return new_product
