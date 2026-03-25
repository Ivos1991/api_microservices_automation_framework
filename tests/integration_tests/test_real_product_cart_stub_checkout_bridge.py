import allure
import pytest
from assertpy import assert_that

from framework.config.config_manager import ConfigManager
from services.cart_service.cart_service import add_item_to_cart, get_cart
from services.cart_service.cart_service_models import AddItemRequest
from services.checkout_service.checkout_service import checkout_cart
from services.checkout_service.checkout_service_models import CheckoutCartRequest, ShippingAddress
from services.product_catalog_service.product_catalog_service import get_product_by_id
from services.product_catalog_service.product_catalog_service_models import GetProductByIdRequest


@allure.parent_suite("Integration Tests")
@allure.suite("Hybrid Product Cart Checkout")
@allure.sub_suite("real product and cart with stub checkout bridge")
@pytest.mark.integration_test
@pytest.mark.real_target
@pytest.mark.product_catalog_service
@pytest.mark.cart_service
@pytest.mark.checkout_service
def test_real_product_and_cart_can_feed_stub_checkout_via_explicit_bridge(cart_stub_server, real_product_cart_config):
    stub_config = ConfigManager(
        overrides={
            "framework_profile": "stub",
            "default_service_backend": "stub",
            "product_catalog_service_backend": "stub",
            "cart_service_backend": "stub",
            "checkout_service_backend": "stub",
            "product_catalog_service_stub_base_url": cart_stub_server.base_url,
            "cart_service_stub_base_url": cart_stub_server.base_url,
            "checkout_service_stub_base_url": cart_stub_server.base_url,
        }
    )

    product = get_product_by_id(
        config=real_product_cart_config,
        request=GetProductByIdRequest(product_id=real_product_cart_config.default_product_id),
    )
    real_request = AddItemRequest(
        user_id="codex-hybrid-cart-user",
        product_id=product.product_id,
        quantity=1,
    )
    real_add_result = add_item_to_cart(config=real_product_cart_config, request=real_request)
    real_cart = get_cart(config=real_product_cart_config, user_id=real_request.user_id)

    cart_stub_server.reset()
    add_item_to_cart(
        config=stub_config,
        request=AddItemRequest(
            user_id=real_request.user_id,
            product_id=product.product_id,
            quantity=1,
        ),
    )
    checkout_result = checkout_cart(
        config=stub_config,
        request=CheckoutCartRequest(
            user_id=real_request.user_id,
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

    assert_that(real_add_result.status).is_equal_to("OK")
    assert_that(real_cart.user_id).is_equal_to(real_request.user_id)
    assert_that([item.product_id for item in real_cart.items]).contains(product.product_id)
    assert_that(checkout_result.order_id).is_not_empty()
    assert_that(checkout_result.items[0].product_id).is_equal_to(product.product_id)
