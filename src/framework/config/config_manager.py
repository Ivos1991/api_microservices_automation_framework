from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import os

from dotenv import load_dotenv


def _to_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    framework_profile: str
    default_service_backend: str
    cart_service_backend: str
    product_catalog_service_backend: str
    checkout_service_backend: str
    target_env: str
    request_timeout_seconds: int
    verify_ssl: bool
    allure_attach_http: bool
    cart_service_stub_base_url: str
    cart_service_real_base_url: str
    product_catalog_service_stub_base_url: str
    product_catalog_service_real_base_url: str
    checkout_service_stub_base_url: str
    checkout_service_real_base_url: str
    default_cart_user_id: str
    default_product_id: str
    default_product_quantity: int


class ConfigManager:
    """Small environment-driven config object for the framework."""

    def __init__(self, env_file: str = ".env", overrides: dict[str, Any] | None = None):
        root_dir = Path(__file__).resolve().parents[3]
        load_dotenv(root_dir / env_file, override=False)
        merged = {**self._read_env(), **(overrides or {})}
        self._settings = Settings(**merged)

    @staticmethod
    def _read_env() -> dict[str, Any]:
        framework_profile = os.getenv("FRAMEWORK_PROFILE", "stub")
        default_service_backend = os.getenv(
            "DEFAULT_SERVICE_BACKEND",
            "real" if framework_profile == "real" else "stub",
        )
        return {
            "framework_profile": framework_profile,
            "default_service_backend": default_service_backend,
            "cart_service_backend": os.getenv("CART_SERVICE_BACKEND", default_service_backend),
            "product_catalog_service_backend": os.getenv("PRODUCT_CATALOG_SERVICE_BACKEND", default_service_backend),
            "checkout_service_backend": os.getenv("CHECKOUT_SERVICE_BACKEND", default_service_backend),
            "target_env": os.getenv("TARGET_ENV", "local"),
            "request_timeout_seconds": int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10")),
            "verify_ssl": _to_bool(os.getenv("VERIFY_SSL", "false")),
            "allure_attach_http": _to_bool(os.getenv("ALLURE_ATTACH_HTTP", "false")),
            "cart_service_stub_base_url": os.getenv(
                "CART_SERVICE_STUB_BASE_URL",
                os.getenv("CART_SERVICE_BASE_URL", "http://localhost:8081"),
            ),
            "cart_service_real_base_url": os.getenv(
                "CART_SERVICE_REAL_BASE_URL",
                "http://localhost:60003",
            ),
            "product_catalog_service_stub_base_url": os.getenv(
                "PRODUCT_CATALOG_SERVICE_STUB_BASE_URL",
                os.getenv("PRODUCT_CATALOG_SERVICE_BASE_URL", "http://localhost:8081"),
            ),
            "product_catalog_service_real_base_url": os.getenv(
                "PRODUCT_CATALOG_SERVICE_REAL_BASE_URL",
                "http://localhost:60002",
            ),
            "checkout_service_stub_base_url": os.getenv(
                "CHECKOUT_SERVICE_STUB_BASE_URL",
                os.getenv("CHECKOUT_SERVICE_BASE_URL", "http://localhost:8081"),
            ),
            "checkout_service_real_base_url": os.getenv(
                "CHECKOUT_SERVICE_REAL_BASE_URL",
                "http://localhost:60001",
            ),
            "default_cart_user_id": os.getenv("DEFAULT_CART_USER_ID", "demo-user"),
            "default_product_id": os.getenv("DEFAULT_PRODUCT_ID", "OLJCESPC7Z"),
            "default_product_quantity": int(os.getenv("DEFAULT_PRODUCT_QUANTITY", "1")),
        }

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def framework_profile(self) -> str:
        return self._settings.framework_profile

    @property
    def default_service_backend(self) -> str:
        return self._settings.default_service_backend

    @property
    def target_env(self) -> str:
        return self._settings.target_env

    @property
    def request_timeout_seconds(self) -> int:
        return self._settings.request_timeout_seconds

    @property
    def verify_ssl(self) -> bool:
        return self._settings.verify_ssl

    @property
    def allure_attach_http(self) -> bool:
        return self._settings.allure_attach_http

    @property
    def cart_service_base_url(self) -> str:
        return self._resolve_service_base_url("cart_service")

    @property
    def product_catalog_service_base_url(self) -> str:
        return self._resolve_service_base_url("product_catalog_service")

    @property
    def checkout_service_base_url(self) -> str:
        return self._resolve_service_base_url("checkout_service")

    @property
    def default_cart_user_id(self) -> str:
        return self._settings.default_cart_user_id

    @property
    def default_product_id(self) -> str:
        return self._settings.default_product_id

    @property
    def default_product_quantity(self) -> int:
        return self._settings.default_product_quantity

    def service_backend(self, service_name: str) -> str:
        return getattr(self._settings, f"{service_name}_backend")

    def is_real_backend(self, service_name: str) -> bool:
        return self.service_backend(service_name) == "real"

    def _resolve_service_base_url(self, service_name: str) -> str:
        backend = self.service_backend(service_name)
        base_url = getattr(self._settings, f"{service_name}_{backend}_base_url")
        if base_url:
            return base_url
        raise ValueError(
            f"{service_name} is configured for backend '{backend}' but no base URL is set for that backend."
        )
