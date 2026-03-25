import pytest
import requests

from framework.config.config_manager import ConfigManager


@pytest.fixture()
def integration_cart_state(cart_stub_server):
    cart_stub_server.reset()
    try:
        yield
    finally:
        cart_stub_server.reset()


@pytest.fixture()
def real_product_cart_config():
    config = ConfigManager(
        overrides={
            "framework_profile": "real",
            "default_service_backend": "stub",
            "product_catalog_service_backend": "real",
            "cart_service_backend": "real",
            "checkout_service_backend": "stub",
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
            f"{config.cart_service_base_url.rstrip('/')}/cart/user_id/codex-real-cart-readiness",
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
    return config


@pytest.fixture()
def real_product_cart_checkout_config():
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
        pytest.skip(f"real checkout target returned unexpected status {checkout_probe.status_code}")
    return config
