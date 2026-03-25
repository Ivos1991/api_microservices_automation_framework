# API Microservices Automation Framework

This repository demonstrates a backend automation approach built around clear service boundaries, deterministic local execution, and honest live-target verification. It keeps the architecture intentionally small: three service slices, one verified business flow, explicit fixtures, reusable HTTP/reporting infrastructure, and no hidden orchestration.

## Project Summary

Implemented service slices:

- `product_catalog_service`
- `cart_service`
- `checkout_service`

Validated live business flow:

- product -> cart -> checkout

Execution modes:

- stub mode for deterministic local validation
- real-target mode for live verification against the sample microservices runtime

The framework preserves the same service/API/request/test layering in both modes. Only configuration changes.

## Architecture Overview

```text
api-microservices-automation-framework/
|-- docs/
|-- src/
|   |-- framework/
|   |   |-- api/
|   |   |-- config/
|   |   `-- reporting/
|   `-- services/
|       |-- cart_service/
|       |-- checkout_service/
|       `-- product_catalog_service/
|-- tests/
|   |-- integration_tests/
|   |-- services_tests/
|   `-- support/
|-- conftest.py
|-- pytest.ini
`-- README.md
```

### Layering Model

- `*_service.py`
  Orchestrates request building, API execution, thin transport checks, and response normalization.
- `*_service_api.py`
  Owns endpoint paths and HTTP execution through the shared base API layer.
- `*_service_request.py`
  Owns request-body and query construction only.
- `*_service_models.py`
  Holds typed request and response models when they improve clarity.
- tests
  Own business assertions, Allure suite metadata, and explicit scenario setup.

This keeps transport concerns, payload construction, and scenario meaning separated.

## Tech Stack

- Python 3
- `pytest`
- `requests`
- `assertpy`
- `allure-pytest`
- `python-dotenv`

## Implemented Services

### Product Catalog

- Stub route supported
- Real-target route supported
- Real contract normalized behind `get_product_by_id(...)`

### Cart

- Stub route supported
- Real-target route supported
- Request/response differences normalized behind `add_item_to_cart(...)` and `get_cart(...)`

### Checkout

- Stub route supported
- Real-target route supported
- Live checkout request/response differences normalized behind `checkout_cart(...)`

## Stub Mode Vs Real-Target Mode

### Stub Mode

Purpose:

- fast local development
- deterministic regression safety net
- no Docker dependency

Behavior:

- root `conftest.py` starts the local fake runtime
- all services resolve to stub URLs
- service and integration tests run fully local

### Real-Target Mode

Purpose:

- verify live contracts against the running sample microservices runtime
- keep the same framework architecture while switching service backends through config

Behavior:

- per-service backend routing is controlled by environment variables
- the verified live setup uses:
  - `http://localhost:60002` for product catalog
  - `http://localhost:60003` for cart
  - `http://localhost:60001` for checkout
- real-target readiness checks skip cleanly if the runtime is unavailable

Important honesty note:

- the live runtime does not perfectly match the older documented contract in every field
- the framework normalizes those differences instead of hiding them in tests

## Configuration

Key environment variables:

- `FRAMEWORK_PROFILE=stub|real`
- `DEFAULT_SERVICE_BACKEND=stub|real`
- `PRODUCT_CATALOG_SERVICE_BACKEND=stub|real`
- `CART_SERVICE_BACKEND=stub|real`
- `CHECKOUT_SERVICE_BACKEND=stub|real`
- `PRODUCT_CATALOG_SERVICE_STUB_BASE_URL`
- `PRODUCT_CATALOG_SERVICE_REAL_BASE_URL`
- `CART_SERVICE_STUB_BASE_URL`
- `CART_SERVICE_REAL_BASE_URL`
- `CHECKOUT_SERVICE_STUB_BASE_URL`
- `CHECKOUT_SERVICE_REAL_BASE_URL`

Example defaults are provided in [.env.example](.env.example).

## Setup

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Docker Runtime Setup

The live target used by this framework is the cloned sample microservices repo at:

`<your local path>/sample-microservices`

Start the runtime:

```powershell
cd <your local path>/sample-microservices
docker compose -f src/docker-compose.yml -f skyramp/docker/demo/docker-compose.yml up -d
```

Stop the runtime:

```powershell
docker compose -f src/docker-compose.yml -f skyramp/docker/demo/docker-compose.yml down
```

## Running Tests

Run the deterministic stub suite:

```bash
python -m pytest -q -m "not real_target" -p no:cacheprovider
```

Run the live real-target suite:

```bash
python -m pytest -q -m real_target -p no:cacheprovider
```

Run the whole repository:

```bash
python -m pytest -q -p no:cacheprovider
```

## Allure Reporting

Generate results:

```bash
python -m pytest -q --alluredir=allure-results -p no:cacheprovider
```

Open a local report:

```bash
allure serve allure-results
```

Generate static output:

```bash
allure generate allure-results --clean -o allure-report
```

## GitHub Actions

Included workflows:

- `PR Validation`
  Runs the stub-only suite for pull requests and pushes to `main`.
- `Manual Run`
  Lets you trigger `stub`, `real_target`, or `full` execution from GitHub Actions.
- `Nightly Regression`
  Runs the full suite on a schedule and can also be triggered manually.

The reusable workflow starts the real sample microservices runtime only for the jobs that need live verification.

Pipeline features:

- reusable workflow for shared pytest execution
- stub-only PR safety checks
- manual dispatch with selectable execution mode
- scheduled full-regression support
- artifact upload for Allure results

## Design Choices And Limitations

- The scope is intentionally narrow: three service slices and one verified business flow.
- Stub mode remains the primary deterministic regression layer.
- Real-target mode is honest about live runtime behavior instead of forcing the runtime to fit earlier assumptions.
- The live sample runtime currently leaves cart contents intact after checkout, so tests assert observed behavior rather than an assumed side effect.
- The project does not include UI automation, database assertions, or broad multi-service expansion.

## What this project demonstrates:

- service-oriented API automation design
- documentation-first engineering discipline
- contract normalization between stubbed and live systems
- explicit fixture ownership and state handling
- realistic backend integration testing with controlled scope
- honest reporting of validated behavior and known limitations

## Supporting Docs

- [architecture overview](docs/architecture-overview.md)
- [testing strategy](docs/testing-strategy.md)
- [real runtime setup](docs/real-runtime-setup.md)
- [execution model](docs/execution-model.md)
- [known limitations](docs/known-limitations.md)
- [verified live behavior](docs/verified-live-behavior.md)
