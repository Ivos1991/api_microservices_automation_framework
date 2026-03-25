from __future__ import annotations

import json
import threading
import uuid
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


@dataclass
class _CartState:
    products: list[dict] = field(
        default_factory=lambda: [
            {
                "id": "OLJCESPC7Z",
                "name": "Vintage Camera Lens",
                "description": "Demo product for contract-safe service testing.",
                "picture": "https://example.test/images/vintage-camera-lens.png",
                "categories": ["photography", "vintage"],
                "price_usd": {"currency_code": "USD", "units": 129, "nanos": 0},
            },
            {
                "id": "66VCHSJNUP",
                "name": "Desk Organizer",
                "description": "Secondary product for lightweight integration tests.",
                "picture": "https://example.test/images/desk-organizer.png",
                "categories": ["office"],
                "price_usd": {"currency_code": "USD", "units": 24, "nanos": 0},
            },
        ]
    )
    carts: dict[str, list[dict]] = field(default_factory=dict)

    def reset(self) -> None:
        self.carts.clear()

    def add_item(self, user_id: str, product_id: str, quantity: int) -> dict:
        items = self.carts.setdefault(user_id, [])
        for item in items:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                return item
        item = {"product_id": product_id, "quantity": quantity}
        items.append(item)
        return item

    def get_cart(self, user_id: str) -> dict:
        return {"user_id": user_id, "items": list(self.carts.get(user_id, []))}

    def get_product(self, product_id: str) -> dict | None:
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None

    def checkout_cart(self, user_id: str, email: str, shipping_address: dict) -> dict | None:
        items = self.carts.get(user_id, [])
        if not items:
            return None

        order_items = []
        for item in items:
            product = self.get_product(item["product_id"])
            product_name = product["name"] if product is not None else item["product_id"]
            order_items.append(
                {
                    "product_id": item["product_id"],
                    "product_name": product_name,
                    "quantity": item["quantity"],
                }
            )

        return {
            "order_id": str(uuid.uuid4()),
            "user_id": user_id,
            "email": email,
            "status": "CHECKOUT_COMPLETED",
            "items": order_items,
            "shipping_address": shipping_address,
        }


class FakeCartServiceServer:
    def __init__(self):
        self._state = _CartState()
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None
        self.base_url: str | None = None

    def start(self) -> None:
        state = self._state

        class Handler(BaseHTTPRequestHandler):
            def _send_json(self, payload: dict, status_code: int = 200) -> None:
                body = json.dumps(payload).encode("utf-8")
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self) -> None:
                if self.path.startswith("/checkout/user_id/"):
                    user_id = self.path.rsplit("/", 1)[-1]
                    content_length = int(self.headers.get("Content-Length", "0"))
                    raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
                    request_json = json.loads(raw_body)
                    order = state.checkout_cart(
                        user_id=user_id,
                        email=request_json["email"],
                        shipping_address=request_json["shipping_address"],
                    )
                    if order is None:
                        self._send_json({"error": "cart is empty"}, 400)
                        return
                    self._send_json(order)
                    return
                if not self.path.startswith("/cart/user_id/"):
                    self._send_json({"error": "not found"}, 404)
                    return
                user_id = self.path.rsplit("/", 1)[-1]
                content_length = int(self.headers.get("Content-Length", "0"))
                raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
                request_json = json.loads(raw_body)
                item_data = request_json["item"]
                stored_item = state.add_item(
                    user_id=user_id,
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"],
                )
                self._send_json({"status": "OK", "user_id": user_id, "item": stored_item})

            def do_GET(self) -> None:
                if self.path.startswith("/products/"):
                    product_id = self.path.rsplit("/", 1)[-1]
                    product = state.get_product(product_id)
                    if product is None:
                        self._send_json({"error": "not found"}, 404)
                        return
                    self._send_json(product)
                    return
                if not self.path.startswith("/cart/user_id/"):
                    self._send_json({"error": "not found"}, 404)
                    return
                user_id = self.path.rsplit("/", 1)[-1]
                self._send_json(state.get_cart(user_id))

            def log_message(self, format: str, *args) -> None:
                return

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        host, port = self._server.server_address
        self.base_url = f"http://{host}:{port}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def reset(self) -> None:
        self._state.reset()

    def stop(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)
