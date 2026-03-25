import allure
import pytest
from assertpy import assert_that

from services.cart_service.cart_service import add_item_to_cart


@allure.parent_suite("Services Tests")
@allure.suite("Cart Service")
@allure.sub_suite("add item to cart")
@pytest.mark.services_test
@pytest.mark.cart_service
class TestAddItemToCart:
    def test_add_item_to_cart_returns_ok_status(self, config, cart_item_request):
        result = add_item_to_cart(config=config, request=cart_item_request)

        assert_that(result.status).is_equal_to("OK")
        assert_that(result.user_id).is_equal_to(cart_item_request.user_id)
        assert_that(result.item.product_id).is_equal_to(cart_item_request.product_id)
        assert_that(result.item.quantity).is_equal_to(cart_item_request.quantity)
