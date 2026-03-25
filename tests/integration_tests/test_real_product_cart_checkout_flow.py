import allure
import pytest
from assertpy import assert_that

from services.cart_service.cart_service import add_item_to_cart, get_cart
from services.cart_service.cart_service_models import AddItemRequest
from services.checkout_service.checkout_service import checkout_cart
from services.checkout_service.checkout_service_models import CheckoutCartRequest, ShippingAddress
from services.product_catalog_service.product_catalog_service import get_product_by_id
from services.product_catalog_service.product_catalog_service_models import GetProductByIdRequest


@allure.parent_suite("Integration Tests")
@allure.suite("Real Product Cart Checkout")
@allure.sub_suite("product to cart to checkout")
@pytest.mark.integration_test
@pytest.mark.real_target
@pytest.mark.product_catalog_service
@pytest.mark.cart_service
@pytest.mark.checkout_service
def test_real_product_cart_checkout_flow(real_product_cart_checkout_config):
    product = get_product_by_id(
        config=real_product_cart_checkout_config,
        request=GetProductByIdRequest(product_id=real_product_cart_checkout_config.default_product_id),
    )
    add_request = AddItemRequest(
        user_id="codex-real-flow-user",
        product_id=product.product_id,
        quantity=1,
    )
    add_result = add_item_to_cart(config=real_product_cart_checkout_config, request=add_request)
    cart_before_checkout = get_cart(config=real_product_cart_checkout_config, user_id=add_request.user_id)
    checkout_result = checkout_cart(
        config=real_product_cart_checkout_config,
        request=CheckoutCartRequest(
            user_id=add_request.user_id,
            email="buyer@example.test",
            shipping_address=ShippingAddress(
                street_address="1600 Amp street",
                city="Mountain View",
                state="CA",
                zip_code="94043",
                country="USA",
            ),
        ),
    )
    cart_after_checkout = get_cart(config=real_product_cart_checkout_config, user_id=add_request.user_id)

    assert_that(product.product_id).is_equal_to(add_request.product_id)
    assert_that(add_result.status).is_equal_to("OK")
    assert_that(cart_before_checkout.items).is_not_empty()
    assert_that(checkout_result.order_id).is_not_empty()
    assert_that(checkout_result.shipping_tracking_id).is_not_empty()
    assert_that(len(checkout_result.items)).is_greater_than(0)
    assert_that(checkout_result.items[0].product_id).is_equal_to(product.product_id)
    assert_that(cart_after_checkout.items).is_not_empty()
    assert_that([item.product_id for item in cart_after_checkout.items]).contains(product.product_id)
