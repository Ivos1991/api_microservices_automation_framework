import allure
import pytest
from assertpy import assert_that

from services.checkout_service.checkout_service import checkout_cart


@allure.parent_suite("Services Tests")
@allure.suite("Checkout Service")
@allure.sub_suite("checkout cart real target")
@pytest.mark.services_test
@pytest.mark.checkout_service
@pytest.mark.real_target
class TestCheckoutCartRealTarget:
    def test_checkout_cart_against_real_target(self, real_checkout_config, real_checkout_cart_request):
        result = checkout_cart(config=real_checkout_config, request=real_checkout_cart_request)

        assert_that(result.order_id).is_not_empty()
        assert_that(result.user_id).is_equal_to(real_checkout_cart_request.user_id)
        assert_that(result.email).is_equal_to(real_checkout_cart_request.email)
        assert_that(result.status).is_equal_to("CHECKOUT_COMPLETED")
        assert_that(result.shipping_tracking_id).is_not_empty()
        assert_that(result.shipping_cost).is_not_none()
        assert_that(result.shipping_cost.currency_code).is_equal_to("USD")
        assert_that(len(result.items)).is_greater_than(0)
        assert_that(result.items[0].product_id).is_not_empty()
