from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GetProductByIdRequest:
    product_id: str


@dataclass(frozen=True)
class ProductPrice:
    currency_code: str
    units: int
    nanos: int


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    description: str
    picture_url: str
    categories: list[str]
    price: ProductPrice
