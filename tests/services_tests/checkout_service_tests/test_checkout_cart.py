import allure
import pytest
from assertpy import assert_that

from services.checkout_service.checkout_service import checkout_cart


@allure.parent_suite("Services Tests")
@allure.suite("Checkout Service")
@allure.sub_suite("checkout cart")
@pytest.mark.services_test
@pytest.mark.checkout_service
class TestCheckoutCart:
    def test_checkout_cart_returns_order_for_seeded_cart(self, config, checkout_cart_request):
        result = checkout_cart(config=config, request=checkout_cart_request)

        assert_that(result.order_id).is_not_empty()
        assert_that(result.user_id).is_equal_to(checkout_cart_request.user_id)
        assert_that(result.email).is_equal_to(checkout_cart_request.email)
        assert_that(result.status).is_equal_to("CHECKOUT_COMPLETED")
        assert_that(len(result.items)).is_equal_to(1)
        assert_that(result.shipping_address.country).is_equal_to("US")
