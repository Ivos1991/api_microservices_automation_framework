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
@allure.suite("Product Catalog Cart And Checkout")
@allure.sub_suite("product to cart to checkout")
@pytest.mark.integration_test
@pytest.mark.cart_service
@pytest.mark.checkout_service
@pytest.mark.product_catalog_service
def test_product_cart_checkout_flow_returns_order(config, integration_cart_state):
    product = get_product_by_id(
        config=config,
        request=GetProductByIdRequest(product_id=config.default_product_id),
    )
    add_request = AddItemRequest(
        user_id=config.default_cart_user_id,
        product_id=product.product_id,
        quantity=config.default_product_quantity,
    )

    add_result = add_item_to_cart(config=config, request=add_request)
    cart = get_cart(config=config, user_id=add_request.user_id)
    checkout_result = checkout_cart(
        config=config,
        request=CheckoutCartRequest(
            user_id=add_request.user_id,
            email="buyer@example.test",
            shipping_address=ShippingAddress(
                street_address="100 Market Street",
                city="Springfield",
                state="IL",
                zip_code="62701",
                country="US",
            ),
        ),
    )

    assert_that(product.name).is_not_empty()
    assert_that(add_result.status).is_equal_to("OK")
    assert_that(cart.user_id).is_equal_to(add_request.user_id)
    assert_that(len(cart.items)).is_equal_to(1)
    assert_that(cart.items[0].product_id).is_equal_to(product.product_id)
    assert_that(cart.items[0].quantity).is_equal_to(add_request.quantity)
    assert_that(checkout_result.order_id).is_not_empty()
    assert_that(checkout_result.user_id).is_equal_to(add_request.user_id)
    assert_that(checkout_result.status).is_equal_to("CHECKOUT_COMPLETED")
    assert_that(len(checkout_result.items)).is_equal_to(1)
    assert_that(checkout_result.items[0].product_id).is_equal_to(product.product_id)
