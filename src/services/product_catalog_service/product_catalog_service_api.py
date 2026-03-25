from __future__ import annotations

from framework.api.base_api import BaseAPI
from framework.config.config_manager import ConfigManager


class ProductCatalogServiceAPI(BaseAPI):
    def __init__(self, config: ConfigManager):
        self.config = config
        super().__init__(
            base_url=config.product_catalog_service_base_url,
            timeout_seconds=config.request_timeout_seconds,
            verify_ssl=config.verify_ssl,
            attach_http=config.allure_attach_http,
        )

    def get_product_by_id(self, product_id: str):
        if self.config.is_real_backend("product_catalog_service"):
            return self.execute("get", "/get-product", params={"product_id": product_id})
        return self.execute("get", f"/products/{product_id}")
