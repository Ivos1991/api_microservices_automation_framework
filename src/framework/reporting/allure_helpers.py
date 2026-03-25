from __future__ import annotations

import json
from typing import Any

import allure


def attach_json(name: str, payload: Any) -> None:
    allure.attach(
        json.dumps(payload, indent=2, sort_keys=True),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_http_exchange(name: str, request_summary: dict[str, Any], response_summary: dict[str, Any]) -> None:
    attach_json(f"{name} request", request_summary)
    attach_json(f"{name} response", response_summary)
