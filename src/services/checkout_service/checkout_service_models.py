from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ShippingAddress:
    street_address: str
    city: str
    state: str
    zip_code: str
    country: str


@dataclass(frozen=True)
class CreditCardInfo:
    credit_card_number: str = "4432-8015-6251-0454"
    credit_card_cvv: int = 672
    credit_card_expiration_year: int = 2029
    credit_card_expiration_month: int = 1


@dataclass(frozen=True)
class CheckoutMoney:
    currency_code: str
    units: int
    nanos: int


@dataclass(frozen=True)
class CheckoutCartRequest:
    user_id: str
    email: str
    shipping_address: ShippingAddress
    user_currency: str = "USD"
    credit_card: CreditCardInfo = field(default_factory=CreditCardInfo)


@dataclass(frozen=True)
class CheckoutItem:
    product_id: str
    product_name: str | None
    quantity: int
    cost: CheckoutMoney | None = None


@dataclass(frozen=True)
class CheckoutOrder:
    order_id: str
    user_id: str | None
    email: str | None
    status: str | None
    items: list[CheckoutItem]
    shipping_address: ShippingAddress
    shipping_tracking_id: str | None = None
    shipping_cost: CheckoutMoney | None = None
