import pytest
import requests

from framework.config.config_manager import ConfigManager

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


@pytest.fixture()
def real_checkout_config():
    config = ConfigManager(
        overrides={
            "framework_profile": "real",
            "default_service_backend": "stub",
            "product_catalog_service_backend": "real",
            "cart_service_backend": "real",
            "checkout_service_backend": "real",
        }
    )
    checks = [
        (
            f"{config.product_catalog_service_base_url.rstrip('/')}/get-product",
            {"product_id": config.default_product_id},
            {200, 404},
            "product catalog",
        ),
        (
            f"{config.cart_service_base_url.rstrip('/')}/cart/user_id/codex-real-checkout-readiness",
            None,
            {200, 404},
            "cart",
        ),
    ]
    for url, params, expected_statuses, label in checks:
        try:
            response = requests.get(
                url,
                params=params,
                timeout=config.request_timeout_seconds,
                verify=config.verify_ssl,
            )
        except requests.RequestException as exc:
            pytest.skip(f"real {label} target not reachable: {exc}")
        if response.status_code not in expected_statuses:
            pytest.skip(f"real {label} target returned unexpected status {response.status_code}")

    try:
        checkout_probe = requests.post(
            f"{config.checkout_service_base_url.rstrip('/')}/checkout",
            json={},
            timeout=config.request_timeout_seconds,
            verify=config.verify_ssl,
        )
    except requests.RequestException as exc:
        pytest.skip(f"real checkout target not reachable: {exc}")
    if checkout_probe.status_code not in {400, 422, 500, 501}:
        pytest.skip(
            f"real checkout target returned unexpected status {checkout_probe.status_code} during readiness check"
        )
    return config


@pytest.fixture()
def real_checkout_cart_request(real_checkout_config):
    product = get_product_by_id(
        config=real_checkout_config,
        request=GetProductByIdRequest(product_id=real_checkout_config.default_product_id),
    )
    add_item_to_cart(
        config=real_checkout_config,
        request=AddItemRequest(
            user_id="codex-real-checkout-user",
            product_id=product.product_id,
            quantity=1,
        ),
    )
    return CheckoutCartRequest(
        user_id="codex-real-checkout-user",
        email="buyer@example.test",
        shipping_address=ShippingAddress(
            street_address="1600 Amp street",
            city="Mountain View",
            state="CA",
            zip_code="94043",
            country="USA",
        ),
    )
