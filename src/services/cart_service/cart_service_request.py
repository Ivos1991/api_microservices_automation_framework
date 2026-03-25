from __future__ import annotations

from services.cart_service.cart_service_models import AddItemRequest


class CartServiceRequest:
    @staticmethod
    def add_item_request(request: AddItemRequest, backend: str) -> dict:
        if backend == "real":
            return {
                "product_id": request.product_id,
                "quantity": request.quantity,
            }
        return {
            "item": {
                "product_id": request.product_id,
                "quantity": request.quantity,
            }
        }
