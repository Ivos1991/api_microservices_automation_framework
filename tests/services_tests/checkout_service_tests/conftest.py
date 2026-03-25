import pytest

from services.cart_service.cart_service import add_item_to_cart
from services.cart_service.cart_service_models import AddItemRequest
from services.checkout_service.checkout_service_models import CheckoutCartRequest, ShippingAddress
from services.product_catalog_service.product_catalog_service import get_product_by_id
from services.product_catalog_service.product_catalog_service_models import GetProductByIdRequest


@pytest.fixture()
def checkout_service_test_state(cart_stub_server):
    cart_stub_server.reset()
    try:
        yield
    finally:
        cart_stub_server.reset()


@pytest.fixture()
def checkout_cart_request(config, checkout_service_test_state):
    product = get_product_by_id(
        config=config,
        request=GetProductByIdRequest(product_id=config.default_product_id),
    )
    add_item_to_cart(
        config=config,
        request=AddItemRequest(
            user_id=config.default_cart_user_id,
            product_id=product.product_id,
            quantity=config.default_product_quantity,
        ),
    )
    return CheckoutCartRequest(
        user_id=config.default_cart_user_id,
        email="buyer@example.test",
        shipping_address=ShippingAddress(
            street_address="100 Market Street",
            city="Springfield",
            state="IL",
            zip_code="62701",
            country="US",
        ),
    )
