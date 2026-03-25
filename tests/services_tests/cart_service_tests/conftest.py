import pytest
import requests

from framework.config.config_manager import ConfigManager

from services.cart_service.cart_service_models import AddItemRequest


@pytest.fixture()
def cart_service_test_state(cart_stub_server):
    cart_stub_server.reset()
    try:
        yield
    finally:
        cart_stub_server.reset()


@pytest.fixture()
def cart_item_request(config, cart_service_test_state):
    return AddItemRequest(
        user_id=config.default_cart_user_id,
        product_id=config.default_product_id,
        quantity=config.default_product_quantity,
    )


@pytest.fixture()
def real_cart_config():
    config = ConfigManager(
        overrides={
            "framework_profile": "real",
            "default_service_backend": "stub",
            "product_catalog_service_backend": "real",
            "cart_service_backend": "real",
            "checkout_service_backend": "stub",
        }
    )
    base_url = config.cart_service_base_url.rstrip("/")
    readiness_user = "codex-real-cart-readiness"
    try:
        response = requests.get(
            f"{base_url}/cart/user_id/{readiness_user}",
            timeout=config.request_timeout_seconds,
            verify=config.verify_ssl,
        )
    except requests.RequestException as exc:
        pytest.skip(f"real cart target not reachable: {exc}")
    if response.status_code not in {200, 404}:
        pytest.skip(f"real cart target returned unexpected status {response.status_code} during readiness check")
    return config


@pytest.fixture()
def real_cart_item_request(real_cart_config):
    return AddItemRequest(
        user_id="codex-real-cart-user",
        product_id=real_cart_config.default_product_id,
        quantity=1,
    )
