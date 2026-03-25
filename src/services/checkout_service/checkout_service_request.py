from __future__ import annotations

from services.checkout_service.checkout_service_models import CheckoutCartRequest


class CheckoutServiceRequest:
    @staticmethod
    def checkout_cart_request(request: CheckoutCartRequest) -> dict:
        return {
            "email": request.email,
            "shipping_address": {
                "street_address": request.shipping_address.street_address,
                "city": request.shipping_address.city,
                "state": request.shipping_address.state,
                "zip_code": request.shipping_address.zip_code,
                "country": request.shipping_address.country,
            },
        }
