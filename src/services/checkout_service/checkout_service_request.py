from __future__ import annotations

from services.checkout_service.checkout_service_models import CheckoutCartRequest


class CheckoutServiceRequest:
    @staticmethod
    def checkout_cart_request(request: CheckoutCartRequest, backend: str) -> dict:
        if backend == "real":
            return {
                "user_id": request.user_id,
                "user_currency": request.user_currency,
                "address": {
                    "street_address": request.shipping_address.street_address,
                    "city": request.shipping_address.city,
                    "state": request.shipping_address.state,
                    "zip_code": request.shipping_address.zip_code,
                    "country": request.shipping_address.country,
                },
                "email": request.email,
                "credit_card": {
                    "credit_card_number": request.credit_card.credit_card_number,
                    "credit_card_cvv": request.credit_card.credit_card_cvv,
                    "credit_card_expiration_year": request.credit_card.credit_card_expiration_year,
                    "credit_card_expiration_month": request.credit_card.credit_card_expiration_month,
                },
            }
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
