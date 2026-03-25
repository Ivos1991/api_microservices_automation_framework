from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShippingAddress:
    street_address: str
    city: str
    state: str
    zip_code: str
    country: str


@dataclass(frozen=True)
class CheckoutCartRequest:
    user_id: str
    email: str
    shipping_address: ShippingAddress


@dataclass(frozen=True)
class CheckoutItem:
    product_id: str
    product_name: str
    quantity: int


@dataclass(frozen=True)
class CheckoutOrder:
    order_id: str
    user_id: str
    email: str
    status: str
    items: list[CheckoutItem]
    shipping_address: ShippingAddress
