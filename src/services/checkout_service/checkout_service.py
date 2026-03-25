from __future__ import annotations

from framework.config.config_manager import ConfigManager
from services.checkout_service.checkout_service_api import CheckoutServiceAPI
from services.checkout_service.checkout_service_models import (
    CheckoutMoney,
    CheckoutCartRequest,
    CheckoutItem,
    CheckoutOrder,
    ShippingAddress,
)
from services.checkout_service.checkout_service_request import CheckoutServiceRequest


def _get_required_value(payload: dict, *keys: str):
    for key in keys:
        if key in payload:
            return payload[key]
    raise KeyError(keys[0])


def _get_optional_value(payload: dict, *keys: str):
    for key in keys:
        if key in payload:
            return payload[key]
    return None


def checkout_cart(config: ConfigManager, request: CheckoutCartRequest) -> CheckoutOrder:
    request_body = CheckoutServiceRequest.checkout_cart_request(
        request=request,
        backend=config.service_backend("checkout_service"),
    )
    response = CheckoutServiceAPI(config).post_checkout_cart(user_id=request.user_id, request_body=request_body)
    assert response.ok, "checkout_service checkout_cart response status not OK"
    response_json = response.json()
    if config.is_real_backend("checkout_service"):
        shipping = _get_required_value(response_json, "shipping_address", "shippingAddress")
        shipping_cost = _get_required_value(response_json, "shipping_cost", "shippingCost")
        return CheckoutOrder(
            order_id=_get_required_value(response_json, "order_id", "orderId"),
            user_id=request.user_id,
            email=request.email,
            status="CHECKOUT_COMPLETED",
            items=[
                CheckoutItem(
                    product_id=_get_required_value(item["item"], "product_id", "productId"),
                    product_name=None,
                    quantity=item["item"]["quantity"],
                    cost=(
                        CheckoutMoney(
                            currency_code=_get_required_value(item_cost, "currency_code", "currencyCode"),
                            units=item_cost["units"],
                            nanos=item_cost["nanos"],
                        )
                        if (item_cost := item.get("cost")) is not None
                        else None
                    ),
                )
                for item in response_json.get("items", [])
            ],
            shipping_address=ShippingAddress(
                street_address=_get_required_value(shipping, "street_address", "streetAddress"),
                city=shipping["city"],
                state=shipping["state"],
                zip_code=_get_optional_value(shipping, "zip_code", "zipCode") or request.shipping_address.zip_code,
                country=shipping["country"],
            ),
            shipping_tracking_id=response_json.get("shipping_tracking_id", response_json.get("shippingTrackingId")),
            shipping_cost=CheckoutMoney(
                currency_code=_get_required_value(shipping_cost, "currency_code", "currencyCode"),
                units=shipping_cost["units"],
                nanos=shipping_cost["nanos"],
            ),
        )
    shipping = response_json["shipping_address"]
    return CheckoutOrder(
        order_id=response_json["order_id"],
        user_id=response_json["user_id"],
        email=response_json["email"],
        status=response_json["status"],
        items=[
            CheckoutItem(
                product_id=item["product_id"],
                product_name=item["product_name"],
                quantity=item["quantity"],
            )
            for item in response_json.get("items", [])
        ],
        shipping_address=ShippingAddress(
            street_address=shipping["street_address"],
            city=shipping["city"],
            state=shipping["state"],
            zip_code=shipping["zip_code"],
            country=shipping["country"],
        ),
    )
