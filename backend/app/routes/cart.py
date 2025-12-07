from typing import Dict

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from ..services.cart import CartService

router = APIRouter(prefix="/api/cart/", tags=["cart"])


class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int
    cart_data: Dict[int, int] = {}


class CartUpdateRequest(BaseModel):
    product_id: int
    quantity: int
    cart_data: Dict[int, int] = {}


class RemoveFromCartRequest(BaseModel):
    product_id: int
    cart_data: Dict[int, int] = {}


@router.post("add/", status_code=status.HTTP_200_OK)
def add_to_cart(request: AddToCartRequest, db: Session = Depends(get_db)):
    cart_service = CartService(db)

    item = CartItemCreate(product_id=request.product_id, quantity=request.quantity)

    updated_cart = cart_service.add_to_cart(request.cart_data, item)

    return {"cart": updated_cart}


@router.post("update/", status_code=status.HTTP_200_OK)
def update_cart(request: CartUpdateRequest, db: Session = Depends(get_db)):
    cart_service = CartService(db)

    item = CartItemUpdate(product_id=request.product_id, quantity=request.quantity)

    updated_cart = cart_service.update_cart_item(request.cart_data, item)

    return {"cart": updated_cart}


@router.post("remove/", status_code=status.HTTP_200_OK)
def remove_from_cart(request: RemoveFromCartRequest, db: Session = Depends(get_db)):
    cart_service = CartService(db)
    updated_cart = cart_service.remove_cart_item(request.cart_data, request.product_id)
    return {"cart": updated_cart}


@router.post("", response_model=CartResponse, status_code=status.HTTP_200_OK)
def get_cart(cart_data: Dict[int, int], db: Session = Depends(get_db)):
    cart_service = CartService(db)

    updated_cart_data = cart_service.get_cart_details(cart_data)

    return {"cart": updated_cart_data}
