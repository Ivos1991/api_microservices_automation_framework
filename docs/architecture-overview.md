# Architecture Overview

## Objective

Present the repository structure and service-layer boundaries in a portfolio-safe way.

## Repository Shape

```text
api-microservices-automation-framework/
|-- docs/
|-- src/
|   |-- framework/
|   |   |-- api/
|   |   |   `-- base_api.py
|   |   |-- config/
|   |   |   `-- config_manager.py
|   |   `-- reporting/
|   |       `-- allure_helpers.py
|   `-- services/
|       |-- cart_service/
|       |-- checkout_service/
|       `-- product_catalog_service/
|-- tests/
|   |-- integration_tests/
|   |-- services_tests/
|   `-- support/
|-- conftest.py
`-- pytest.ini
```

## Framework Layer

### `src/framework/api/base_api.py`

Owns shared HTTP execution:

- requests session creation
- timeout handling
- optional request/response attachment support

### `src/framework/config/config_manager.py`

Owns environment-driven framework configuration:

- profile selection
- per-service backend selection
- service base URL resolution
- timeouts and reporting toggles

### `src/framework/reporting/allure_helpers.py`

Owns reusable Allure attachment helpers.

## Service Layer

Each implemented service slice follows the same shape:

- `*_service.py`
- `*_service_api.py`
- `*_service_request.py`
- `*_service_models.py`

Responsibilities:

- service layer orchestrates and normalizes
- API layer executes endpoints
- request layer builds payloads
- models define typed inputs and outputs

## Test Layer

### `tests/services_tests/`

Single-service validation:

- one slice at a time
- assertions stay in tests
- fixtures stay local to the service domain

### `tests/integration_tests/`

Cross-service validation:

- explicit product -> cart -> checkout composition
- no hidden orchestration inside framework helpers
- runtime-specific assertions stay honest to observed behavior

## Current Scope

Implemented services:

- product catalog
- cart
- checkout

Validated live flow:

- product lookup
- add to cart
- checkout

The repository is intentionally small and does not expand beyond this verified backend flow.
