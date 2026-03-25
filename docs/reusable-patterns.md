# Reusable Patterns

## Structural Patterns To Preserve

### 1. Service Domain Foldering

Group each service domain in one folder:

- `src/services/cart_service/`
- later `src/services/checkout_service/`
- later `src/services/product_catalog_service/`

### 2. Service / API / Request Split

Per service domain, preserve the old repo naming style:

- `cart_service.py`
- `cart_service_api.py`
- `cart_service_request.py`

Add `cart_service_models.py` only when typed request or response contracts improve clarity.

### 3. Test Folder Shape

Preserve the old test hierarchy naming:

- `tests/services_tests/cart_service_tests/`
- `tests/integration_tests/`

### 4. Root And Local Fixture Ownership

Preserve the old split, but keep it cleaner:

- root `conftest.py` owns only infrastructure fixtures such as `config`, shared stub/server wiring, and broad pytest setup
- local `conftest.py` owns domain data, mutable scenario setup, and teardown

### 5. Explicit Config Passing

Preserve the visible `config` fixture pattern from the old repo:

- tests receive `config`
- service methods accept `config`
- APIs resolve service URLs from config

## Patterns To Preserve With Improvement

### Base HTTP Execution

Old pattern to preserve:

- one reusable request executor under the framework layer

Improvement:

- make diagnostics explicit and small
- keep retries and timeouts configurable
- avoid hidden service-specific behavior in the base layer

### Allure Reporting

Old pattern to preserve:

- Allure suites and test annotations live in tests

Improvement:

- keep reusable attachments in `src/framework/reporting/`
- allow technical request/response attachments from the base API only when explicitly enabled

### Request Construction

Old pattern to preserve:

- request payload shaping is separate from execution

Improvement:

- use dataclasses or small typed models where they reduce ambiguity
- keep builders deterministic and free of transport concerns

## Patterns Not To Carry Forward

- oversized root fixture registries
- sprawling config objects unrelated to the current framework scope
- broad custom assertion libraries without real reuse pressure
- mixed business logic, transport, and reporting concerns in one module
