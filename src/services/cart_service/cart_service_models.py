from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AddItemRequest:
    user_id: str
    product_id: str
    quantity: int


@dataclass(frozen=True)
class CartItem:
    product_id: str
    quantity: int


@dataclass(frozen=True)
class AddItemResponse:
    status: str
    user_id: str
    item: CartItem


@dataclass(frozen=True)
class Cart:
    user_id: str
    items: list[CartItem]
