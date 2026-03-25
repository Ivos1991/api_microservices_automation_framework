# Old Repo Reference Audit

## Audited Reference

Primary file:

- `testing_environment/tests/services_tests/cdi_service_tests/test_delete_cdi_transactions_metadata.py`

Old repo used only as a structural reference:

- `C:\Users\Seguras\Downloads\cosas\old_repo\qa-automation_old`

## Import Chain For The Reference Test

### Test Module

`test_delete_cdi_transactions_metadata.py`

Direct imports:

- `allure`
- `pytest`
- `assertpy.assert_that`
- `testing_environment.services.micro_services.cdi_service.cdi_service`

Runtime fixture dependencies:

- `config`
- `existing_transaction_for_delete`

### Local Fixture Module

`testing_environment/tests/services_tests/cdi_service_tests/conftest.py`

Relevant imports in the execution path:

- `ConfigManager`
- `assert_that`
- `get_cdi_metadata_by_transaction_ids`
- `update_cdi_transactions_metadata`
- other CDI service helpers used by sibling fixtures
- `create_organization` and `delete_organization` for broader domain setup in the folder
- `extend_assert_that` from `testing_environment/tests/conftest.py`

The specific fixture used by the audited test is:

- `existing_transaction_for_delete`

Responsibility:

- probe a short list of known transaction ids
- use the CDI service layer to locate a currently existing candidate
- keep the selection logic local to the CDI service test folder

### Root Repo Fixture Module

`conftest.py` at the old repo root

Relevant architectural responsibilities:

- defines the global `config` fixture
- wires pytest CLI options
- sets up report directories
- owns broad test-session behavior

### Shared Testing Fixture Module

`testing_environment/tests/conftest.py`

Relevant responsibilities for the audited path:

- custom `assert_that` extension registration
- shared test utilities
- additional environment-wide fixtures

### Service Layer

`testing_environment/services/micro_services/cdi_service/cdi_service.py`

Relevant functions used by the test:

- `delete_cdi_transactions_metadata(config, transaction_ids)`
- `get_cdi_metadata_by_transaction_ids(config, transaction_ids=None)`

Observed responsibility:

- accept the shared `config` object
- build payloads through `CDIServiceRequest` when needed
- call `CDIServiceAPI`
- assert `response.ok`
- return parsed JSON dictionaries

### Service API Layer

`testing_environment/services/micro_services/cdi_service/cdi_service_api.py`

Relevant methods:

- `get_cdi_metadata_by_transaction_ids`
- `delete_cdi_transactions_metadata`

Observed responsibility:

- subclass `BaseMicroServiceAPI`
- resolve endpoint-specific URLs
- call `super().execute(...)`
- stay very thin

### Request Builder Layer

`testing_environment/services/micro_services/cdi_service/cdi_service_request.py`

Relevant method:

- `delete_cdi_transactions_metadata_request(transaction_ids)`

Observed responsibility:

- build request dictionaries only
- no transport logic
- no assertions

### Request Models Adjacent To The Service

Files such as:

- `get_cdi_accounts_metadata_request.py`
- `update_account_dont_send_to_cdi_request.py`
- `update_cdi_account_holdings_dates_metadata_request.py`
- `update_cdi_account_metadata_request.py`

Observed pattern:

- small dataclasses near the service domain
- typed request inputs used when payloads are not trivial
- not every endpoint is forced into a model

### Service Base Layer

`testing_environment/services/micro_services/base_microservice_api.py`

Observed responsibility:

- extend the generic HTTP base class
- resolve service-specific base URLs using `service_name`
- expose a `health_check`
- optionally add platform-specific headers

### Generic HTTP Base Layer

`core/api/base_api.py`

Observed responsibility:

- execute HTTP requests through `requests`
- centralize timeout handling
- centralize raw request/response logging
- provide optional retry behavior
- stay generic and reusable

### Config Layer

`config/config_manager.py`

Observed responsibility:

- merge config sources from ini files
- expose properties for environment and endpoints
- provide a single config object passed through fixtures and services

## Architecture Hierarchy Used By The Test

```text
root conftest.py
└─ provides config fixture and session infrastructure

testing_environment/tests/services_tests/cdi_service_tests/
├─ conftest.py
│  └─ provides local CDI fixtures such as existing_transaction_for_delete
└─ test_delete_cdi_transactions_metadata.py
   └─ calls cdi_service.py functions

testing_environment/services/micro_services/cdi_service/
├─ cdi_service.py
├─ cdi_service_api.py
├─ cdi_service_request.py
└─ adjacent request dataclasses

testing_environment/services/micro_services/
└─ base_microservice_api.py

core/api/
└─ base_api.py

config/
└─ config_manager.py
```

## Patterns That Should Be Preserved

- `services_tests` naming and domain-grouped test folders
- local `conftest.py` beside the service tests that need scenario fixtures
- root `config` fixture available across the suite
- function-oriented service modules
- thin `*_service_api.py` endpoint wrappers
- payload-only `*_service_request.py` modules
- one reusable base HTTP execution layer
- Allure suite annotations in tests rather than transport modules
- assertions in tests, with only thin response-success checks inside services

## Patterns That Should Be Improved

- keep the new root `conftest.py` much smaller and infrastructure-only
- avoid broad assertion-extension growth unless there is real repeated value
- replace ini-heavy config sprawl with environment-driven settings and explicit overrides
- keep service-specific models small and adjacent to the service folder
- make request/response diagnostics reusable through the framework layer instead of ad hoc helper spread
- avoid carrying company-specific naming or business entities into the new framework

## How The New Repo Should Mirror The Old Structure

The new repository should preserve the old layering shape while remaining cleaner:

### Preserve

- root `config` fixture
- `tests/services_tests/<service>_tests/`
- `tests/integration_tests/`
- `src/services/<service>/`
- `*_service.py`
- `*_service_api.py`
- `*_service_request.py`

### Modernize

- move generic HTTP execution to `src/framework/api/base_api.py`
- move config ownership to `src/framework/config/config_manager.py`
- move reusable Allure helpers to `src/framework/reporting/allure_helpers.py`
- keep the first slice intentionally narrow
- use small dataclasses where contracts benefit from typing

## Implementation Guidance For This Repo

For the new API microservices framework, the first slice should mirror the old CDI structure with a portfolio-safe service domain such as `cart_service`:

- `src/services/cart_service/cart_service.py`
- `src/services/cart_service/cart_service_api.py`
- `src/services/cart_service/cart_service_request.py`
- optional `src/services/cart_service/cart_service_models.py`
- `tests/services_tests/cart_service_tests/`
- `tests/integration_tests/`

This preserves the old hierarchy the user wants while removing the legacy repo's unnecessary breadth.
