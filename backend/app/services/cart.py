from typing import Dict

from app.repositories.product import ProductRepository
from app.schemas.cart import CartItem, CartItemCreate, CartItemUpdate, CartResponse
from app.schemas.product import ProductResponse
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session


class CartService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def add_to_cart(
        self, cart_data: Dict[int, int], item: CartItemCreate
    ) -> Dict[int, int]:
        product = self.product_repository.get_by_id(item.product_id)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        if item.product_id in cart_data:
            cart_data[item.product_id] += item.quantity
        else:
            cart_data[item.product_id] = item.quantity

        return cart_data

    def update_cart_item(
        self, cart_data: Dict[int, int], item: CartItemUpdate
    ) -> Dict[int, int]:
        if item.product_id in cart_data:
            cart_data[item.product_id] = item.quantity
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found in cart",
            )

        return cart_data

    def remove_cart_item(
        self, cart_data: Dict[int, int], product_id: int
    ) -> Dict[int, int]:
        if product_id not in cart_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found in cart",
            )

        del cart_data[product_id]
        return cart_data

    def get_cart_details(self, cart_data: Dict[int, int]) -> CartResponse:
        if not cart_data:
            return CartResponse(items=[], total=0.0, items_count=0)

        products_ids = list(cart_data.keys())
        products = self.product_repository.get_by_ids(products_ids)
        validated_products = [ProductResponse.model_validate(pr) for pr in products]
        products_dict = {pr.id: pr for pr in validated_products}

        items = []
        total_price = 0.0
        items_count = 0

        for product_id, quantity in cart_data.items():
            pr = products_dict[product_id]
            subtotal = pr.price * quantity

            item = CartItem(
                product_id=pr.id,
                name=pr.name,
                subtotal=subtotal,
                quantity=quantity,
                image_url=pr.image_url,
                price=pr.price,
            )
            items.append(item)
            total_price += subtotal
            items_count += 1

        return CartResponse(items=items, total=total_price, items_count=items_count)
