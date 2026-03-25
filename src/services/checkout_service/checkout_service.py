from __future__ import annotations

from framework.config.config_manager import ConfigManager
from services.checkout_service.checkout_service_api import CheckoutServiceAPI
from services.checkout_service.checkout_service_models import (
    CheckoutCartRequest,
    CheckoutItem,
    CheckoutOrder,
    ShippingAddress,
)
from services.checkout_service.checkout_service_request import CheckoutServiceRequest


def checkout_cart(config: ConfigManager, request: CheckoutCartRequest) -> CheckoutOrder:
    request_body = CheckoutServiceRequest.checkout_cart_request(request)
    response = CheckoutServiceAPI(config).post_checkout_cart(user_id=request.user_id, request_body=request_body)
    assert response.ok, "checkout_service checkout_cart response status not OK"
    response_json = response.json()
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
