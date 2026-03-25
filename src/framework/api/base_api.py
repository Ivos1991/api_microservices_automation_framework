from __future__ import annotations

from typing import Any

import requests
from requests import Response, Session

from framework.reporting.allure_helpers import attach_http_exchange


class BaseAPI:
    """Reusable HTTP execution layer for service API modules."""

    def __init__(self, base_url: str, timeout_seconds: int, verify_ssl: bool, attach_http: bool = False):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.verify_ssl = verify_ssl
        self.attach_http = attach_http
        self.session: Session = requests.Session()

    def execute(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Response:
        url = f"{self.base_url}{path}"
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            timeout=self.timeout_seconds,
            verify=self.verify_ssl,
        )
        if self.attach_http:
            attach_http_exchange(
                name=f"{method.upper()} {path}",
                request_summary={"method": method.upper(), "url": url, "params": params, "json": json_body},
                response_summary={
                    "status_code": response.status_code,
                    "json": self._safe_json(response),
                },
            )
        return response

    @staticmethod
    def _safe_json(response: Response) -> Any:
        try:
            return response.json()
        except ValueError:
            return {"text": response.text}
