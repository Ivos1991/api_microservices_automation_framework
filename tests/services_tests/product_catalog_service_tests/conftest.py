import pytest
import requests

from framework.config.config_manager import ConfigManager

from services.product_catalog_service.product_catalog_service_models import GetProductByIdRequest


@pytest.fixture()
def product_catalog_service_test_state(cart_stub_server):
    cart_stub_server.reset()
    try:
        yield
    finally:
        cart_stub_server.reset()


@pytest.fixture()
def product_lookup_request(config, product_catalog_service_test_state):
    return GetProductByIdRequest(product_id=config.default_product_id)


@pytest.fixture()
def real_product_catalog_config():
    config = ConfigManager(
        overrides={
            "framework_profile": "real",
            "default_service_backend": "stub",
            "product_catalog_service_backend": "real",
            "cart_service_backend": "stub",
            "checkout_service_backend": "stub",
        }
    )
    base_url = config.product_catalog_service_base_url.rstrip("/")
    try:
        response = requests.get(
            f"{base_url}/get-product",
            params={"product_id": config.default_product_id},
            timeout=config.request_timeout_seconds,
            verify=config.verify_ssl,
        )
    except requests.RequestException as exc:
        pytest.skip(f"real product catalog target not reachable: {exc}")
    if response.status_code not in {200, 404}:
        pytest.skip(
            f"real product catalog target returned unexpected status {response.status_code} during readiness check"
        )
    return config
