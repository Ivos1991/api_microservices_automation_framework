import allure
import pytest
from assertpy import assert_that

from services.cart_service.cart_service import add_item_to_cart, get_cart


@allure.parent_suite("Services Tests")
@allure.suite("Cart Service")
@allure.sub_suite("add item to cart real target")
@pytest.mark.services_test
@pytest.mark.cart_service
@pytest.mark.real_target
class TestAddItemToCartRealTarget:
    def test_add_item_to_cart_against_real_target(self, real_cart_config, real_cart_item_request):
        add_result = add_item_to_cart(config=real_cart_config, request=real_cart_item_request)
        cart = get_cart(config=real_cart_config, user_id=real_cart_item_request.user_id)

        assert_that(add_result.status).is_equal_to("OK")
        assert_that(add_result.user_id).is_equal_to(real_cart_item_request.user_id)
        assert_that(add_result.item.product_id).is_equal_to(real_cart_item_request.product_id)
        assert_that(cart.user_id).is_equal_to(real_cart_item_request.user_id)
        assert_that(cart.items).is_not_empty()
        assert_that([item.product_id for item in cart.items]).contains(real_cart_item_request.product_id)
