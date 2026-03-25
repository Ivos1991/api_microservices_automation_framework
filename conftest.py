import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from framework.config.config_manager import ConfigManager
from tests.support.fake_cart_service import FakeCartServiceServer


@pytest.fixture(scope="session")
def cart_stub_server():
    server = FakeCartServiceServer()
    server.start()
    try:
        yield server
    finally:
        server.stop()


@pytest.fixture(scope="session")
def config(cart_stub_server):
    return ConfigManager(
        overrides={
            "framework_profile": "stub",
            "default_service_backend": "stub",
            "cart_service_backend": "stub",
            "product_catalog_service_backend": "stub",
            "checkout_service_backend": "stub",
            "target_env": "local-test",
            "cart_service_stub_base_url": cart_stub_server.base_url,
            "product_catalog_service_stub_base_url": cart_stub_server.base_url,
            "checkout_service_stub_base_url": cart_stub_server.base_url,
        }
    )
