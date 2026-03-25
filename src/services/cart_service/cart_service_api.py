from __future__ import annotations

from framework.api.base_api import BaseAPI
from framework.config.config_manager import ConfigManager


class CartServiceAPI(BaseAPI):
    def __init__(self, config: ConfigManager):
        self.config = config
        super().__init__(
            base_url=config.cart_service_base_url,
            timeout_seconds=config.request_timeout_seconds,
            verify_ssl=config.verify_ssl,
            attach_http=config.allure_attach_http,
        )

    def post_add_item(self, user_id: str, request_body: dict):
        return self.execute("post", f"/cart/user_id/{user_id}", json_body=request_body)

    def get_cart(self, user_id: str):
        return self.execute("get", f"/cart/user_id/{user_id}")
