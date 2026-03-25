# Current Reference Analysis

## Primary Legacy Reference

Reference test:

- `testing_environment/tests/services_tests/cdi_service_tests/test_delete_cdi_transactions_metadata.py`

Reference import chain audited for implementation:

1. test module
2. local service-test `conftest.py`
3. root repo `conftest.py`
4. `cdi_service.py`
5. `cdi_service_api.py`
6. `cdi_service_request.py`
7. request dataclasses for related CDI operations
8. `base_microservice_api.py`
9. `core/api/base_api.py`
10. `config/config_manager.py`

## What The Old Test Actually Demonstrates

The reference test is small, but its execution path is structurally opinionated:

- tests live under `tests/services_tests/<domain>_tests/`
- domain-specific setup lives in a local `conftest.py`
- a root `config` fixture is available globally
- the test calls service-layer functions, not transport methods
- the service module orchestrates request builders and API calls
- the service API module owns endpoint names and URL composition
- the request module owns payload shaping only
- shared transport behavior is inherited from a base HTTP layer
- assertions remain in tests, while service modules keep only basic response-OK guards

## Fixture Hierarchy Observed

### Root `conftest.py`

Broad test-environment ownership in the old repo:

- CLI options
- `config` fixture
- session reporting setup
- global logging and environment behavior

### Local `conftest.py`

Service-domain ownership in the old repo:

- scenario data selection
- setup and teardown for mutable test state
- domain-specific helper assertions
- fixture naming that reflects business intent

For the audited test specifically, `existing_transaction_for_delete` stays local to the CDI service test folder and does not leak into a shared fixture registry.

## Layer Responsibilities Confirmed

### `*_service.py`

- exposes test-facing functions
- accepts the shared `config` object
- delegates payload building to `*_service_request.py` where needed
- delegates HTTP execution to `*_service_api.py`
- performs thin transport-success checks
- returns parsed JSON or focused domain data

### `*_service_api.py`

- subclasses a service-specific base API
- maps one method to one endpoint
- constructs URLs
- calls the shared execute method
- stays very thin

### `*_service_request.py`

- transforms typed request inputs into request dictionaries
- keeps payload construction separate from endpoint calls
- does not execute requests

## Config And Base HTTP Structure

### Old Config Pattern

`ConfigManager` is a large property-based configuration object sourced from ini files and environment selection. The useful architectural idea is the single explicit config object passed through tests and services.

### Old HTTP Pattern

`BaseRestApi` centralizes:

- request execution
- timeout handling
- raw request/response logging
- optional retry behavior

`BaseMicroServiceAPI` adds service-name-based URL resolution on top of the shared executor.

## Naming, Assertions, And Allure

Patterns worth preserving:

- `services_tests` directory naming
- `<domain>_service.py`, `<domain>_service_api.py`, `<domain>_service_request.py`
- class-level Allure suite annotations in tests
- `config` fixture name
- explicit fixture names tied to scenario meaning
- tests using readable business assertions

Patterns to improve:

- keep the root `conftest.py` infrastructure-focused and smaller
- keep custom assertion extensions limited and justified
- replace oversized config-property sprawl with a smaller environment-driven config manager
- keep Allure helpers framework-owned instead of mixing attachment logic across the codebase
- use typed models only where they clarify contracts

## New Repo Direction

The new framework should preserve the old repo's visible hierarchy and execution style while tightening boundaries:

- root `conftest.py` for shared infrastructure only
- local `conftest.py` files for service and integration slices
- `src/framework/config/config_manager.py` for explicit environment-driven settings
- `src/framework/api/base_api.py` for reusable HTTP execution
- `src/services/<domain>/` for service, API, request, and optional models
- `tests/services_tests/` for single-domain service behavior
- `tests/integration_tests/` for cross-step or cross-domain behavior
