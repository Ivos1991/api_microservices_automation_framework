from __future__ import annotations

from framework.config.config_manager import ConfigManager
from services.cart_service.cart_service_api import CartServiceAPI
from services.cart_service.cart_service_models import AddItemRequest, AddItemResponse, Cart, CartItem
from services.cart_service.cart_service_request import CartServiceRequest


def add_item_to_cart(config: ConfigManager, request: AddItemRequest) -> AddItemResponse:
    request_body = CartServiceRequest.add_item_request(
        request=request,
        backend=config.service_backend("cart_service"),
    )
    response = CartServiceAPI(config).post_add_item(user_id=request.user_id, request_body=request_body)
    assert response.ok, "cart_service add_item response status not OK"
    response_json = response.json()
    if config.is_real_backend("cart_service"):
        return AddItemResponse(
            status="OK" if response_json.get("success") == "200 OK" else response.reason,
            user_id=request.user_id,
            item=CartItem(
                product_id=request.product_id,
                quantity=request.quantity,
            ),
        )
    return AddItemResponse(
        status=response_json["status"],
        user_id=response_json["user_id"],
        item=CartItem(
            product_id=response_json["item"]["product_id"],
            quantity=response_json["item"]["quantity"],
        ),
    )


def get_cart(config: ConfigManager, user_id: str) -> Cart:
    response = CartServiceAPI(config).get_cart(user_id=user_id)
    assert response.ok, "cart_service get_cart response status not OK"
    response_json = response.json()
    return Cart(
        user_id=response_json["user_id"],
        items=[
            CartItem(product_id=item["product_id"], quantity=item["quantity"])
            for item in response_json.get("items", [])
        ],
    )
