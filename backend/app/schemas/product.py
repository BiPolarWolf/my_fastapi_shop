from typing import Optional

from pydantic import BaseModel, Field

from .category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100, description="Product name")
    description: Optional[str] = Field(
        None, min_length=10, max_length=500, description="Product description"
    )
    price: float = Field(..., gt=0, description="Product price")
    category_id: int = Field(..., description="Category ID")
    image_url: Optional[str] = Field(None, description="Product image URL")


class ProductCreate(ProductBase):
    pass


class ProductResponse(BaseModel):
    id: int = Field(..., description="Product ID")
    name: str
    description: Optional[str]
    price: float
    category_id: int
    category: CategoryResponse = Field(..., description="Product Category Details")
    image_url: Optional[str]


class ProductResponseList(BaseModel):
    products: list[ProductResponse]
    total: int = Field(..., description="Total number of products")
