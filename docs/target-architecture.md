# Target Architecture

## Goal

Keep a clean API-first automation framework with stable service boundaries and honest support for both stub and live execution.

## Repository Shape

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
`-- README.md
```

## Layer Ownership

### `src/framework`

Framework-owned technical concerns:

- config loading
- shared HTTP execution
- reusable Allure helpers

### `src/services`

Service-domain concerns:

- request construction
- endpoint mapping
- service orchestration
- response normalization

### `tests/services_tests`

Single-slice verification:

- one service slice at a time
- explicit local fixtures
- business assertions in tests

### `tests/integration_tests`

Cross-service verification:

- explicit product -> cart -> checkout composition
- visible state setup and retrieval
- no hidden scenario logic in service modules

## Execution Profiles

The framework supports:

- deterministic stub execution
- real-target execution through explicit per-service backend routing

Service modules do not change between profiles. Configuration selects the backend.

## Current Scope

Implemented slices:

- `product_catalog_service`
- `cart_service`
- `checkout_service`

Validated modes:

- all-stub local baseline
- real-target service verification for product catalog, cart, and checkout
- real product -> real cart -> real checkout integration flow
- real product + real cart + stub checkout bridge flow

## Deliberate Improvements Over The Old Repo

- smaller root fixture surface
- explicit environment-driven config manager
- reusable but bounded HTTP diagnostics
- typed models only where they improve clarity
- documentation aligned to verified runtime behavior
