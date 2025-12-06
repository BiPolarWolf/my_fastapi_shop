from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repositories.category import CategoryRepository
from ..repositories.product import ProductRepository
from ..schemas.product import ProductCreate, ProductResponse, ProductResponseList


class CategoryService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_products_all(self) -> ProductResponseList:
        products = self.product_repository.get_all()
        validated_products = [
            ProductResponse.model_validate(product) for product in products
        ]
        return ProductResponseList(
            products=validated_products, total=len(validated_products)
        )

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return ProductResponse.model_validate(product)

    def get_products_by_category(self, cat_id: int) -> ProductResponseList:
        category = self.category_repository.get_by_id(cat_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        products = self.product_repository.get_by_category(cat_id)
        validated_products = [
            ProductResponse.model_validate(product) for product in products
        ]
        return ProductResponseList(
            products=validated_products, total=len(validated_products)
        )

    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        category = self.category_repository.get_by_id(product_data.category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        product = self.product_repository.create(product_data)
        validated_product = ProductResponse.model_validate(product)

        return validated_product
