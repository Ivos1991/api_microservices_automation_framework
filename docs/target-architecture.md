# Target Architecture

## Goal

Build a clean API-first microservices automation framework that preserves the old service-test hierarchy while modernizing the framework layer.

## Repository Shape

```text
api-microservices-automation-framework/
├─ AGENTS.md
├─ .env.example
├─ .gitignore
├─ conftest.py
├─ pytest.ini
├─ requirements.txt
├─ README.md
├─ docs/
├─ src/
│  ├─ framework/
│  │  ├─ api/
│  │  │  └─ base_api.py
│  │  ├─ config/
│  │  │  └─ config_manager.py
│  │  └─ reporting/
│  │     └─ allure_helpers.py
│  └─ services/
│     ├─ cart_service/
│     ├─ product_catalog_service/
│     └─ checkout_service/
├─ tests/
│  ├─ support/
│  ├─ services_tests/
│  │  ├─ cart_service_tests/
│  │  ├─ product_catalog_service_tests/
│  │  └─ checkout_service_tests/
│  └─ integration_tests/
└─ artifacts/
```

## Layer Ownership

### `src/framework`

Framework-owned technical infrastructure:

- config loading
- shared HTTP execution
- reusable Allure attachments

### `src/services`

Service-domain behavior:

- request payload construction
- endpoint mapping
- service orchestration
- response parsing

### `tests/services_tests`

Single-domain service behavior:

- one service slice at a time
- local service fixtures
- domain-focused assertions

### `tests/integration_tests`

Cross-step backend validation:

- state before and after mutation
- multi-call flows
- explicit service composition

## Execution Profiles

The framework supports two execution directions without changing service boundaries:

- deterministic stub-first local execution
- incremental real-target execution through explicit per-service backend routing

Service modules do not change between profiles. Only config decides whether a given service points to the local stub or the real target.

## Current Scope

The repository currently implements three portfolio-safe slices:

- `product_catalog_service`
- `cart_service`
- `checkout_service`

These slices support:

- deterministic all-stub local execution
- incremental real-target routing for product catalog and cart
- a stable local hybrid baseline without forcing full migration

## Deliberate Improvements Over The Old Repo

- root `conftest.py` stays small and infrastructure-oriented
- config manager is environment-driven and bounded
- base API diagnostics are reusable and optional
- typed models are limited to the slices that benefit from them
- service and integration layers are kept distinct from the start
