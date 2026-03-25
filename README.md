# API Microservices Automation Framework

API-first microservices automation framework built as a documentation-first portfolio project.

The repository demonstrates a clean service-oriented automation structure inspired by a legacy enterprise test hierarchy, but modernized into a smaller, portfolio-safe framework with:

- explicit `service -> api -> request` layering
- deterministic local stub execution
- incremental real-target onboarding
- reusable Allure reporting helpers
- separate service and integration test layers

## Project Overview

This project targets a microservices demo system and validates backend business flows through service-level automation modules rather than UI-driven orchestration.

Current implemented slices:

- `product_catalog_service`
- `cart_service`
- `checkout_service`

The framework supports two honest operating modes:

- stub mode: fast, deterministic local development and validation
- hybrid/real-target mode: controlled onboarding of real target services without forcing full migration

## Architecture Overview

The project follows a strict layered structure:

```text
src/
├─ framework/
│  ├─ api/
│  ├─ config/
│  └─ reporting/
└─ services/
   ├─ product_catalog_service/
   ├─ cart_service/
   └─ checkout_service/

tests/
├─ services_tests/
└─ integration_tests/
```

### Layering Model

- `*_service.py`
  - orchestration layer used by tests
  - performs thin response validation
  - returns parsed domain-friendly models

- `*_service_api.py`
  - thin transport layer
  - owns endpoint routes and request execution

- `*_service_request.py`
  - payload/query construction only
  - keeps transport and business assertions out of request builders

- tests
  - own business assertions
  - use local fixtures
  - carry Allure suite metadata

## Tech Stack

- Python 3
- `pytest`
- `requests`
- `allure-pytest`
- `assertpy`
- `python-dotenv`

## Implemented Slices

### Product Catalog

- stub mode supported
- real-target routing supported
- real contract mapped to `GET /get-product?product_id=...`

### Cart

- stub mode supported
- real-target routing supported
- real add/get contract normalized behind the service layer

### Checkout

- stub mode supported
- intentionally still stub-only for execution
- retained as the controlled boundary before full real-target migration

## Stub Mode Vs Real-Target Mode

### Stub Mode

Default mode for local development.

Characteristics:

- root `conftest.py` starts a local fake service runtime
- all implemented tests run deterministically
- no external runtime is required

### Real-Target Mode

Opt-in mode for incremental target onboarding.

Characteristics:

- configured through environment variables
- service backends can be switched independently
- currently prepared for:
  - real `product_catalog_service`
  - real `cart_service`
- `checkout_service` remains stubbed by design

## Configuration

Important environment variables:

- `FRAMEWORK_PROFILE=stub|real`
- `DEFAULT_SERVICE_BACKEND=stub|real`
- `PRODUCT_CATALOG_SERVICE_BACKEND=stub|real`
- `CART_SERVICE_BACKEND=stub|real`
- `CHECKOUT_SERVICE_BACKEND=stub|real`
- `*_SERVICE_STUB_BASE_URL`
- `*_SERVICE_REAL_BASE_URL`

Example stub-first configuration is provided in [.env.example](C:/Users/Seguras/Downloads/cosas/ivo_personal/api-microservices-automation-framework/.env.example).

## Running Tests

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the deterministic local suite:

```bash
python -m pytest -q
```

Run only real-target-aware tests:

```bash
python -m pytest -q -m real_target
```

If the real target runtime is not reachable, those tests are designed to skip rather than fail noisily.

## Allure Reporting

Run tests with an Allure results directory:

```bash
python -m pytest --alluredir=allure-results
```

Generate and open the report locally if Allure CLI is installed:

```bash
allure serve allure-results
```

Or generate static output:

```bash
allure generate allure-results --clean -o allure-report
```

## Enabling Real-Target Mode

This repository currently targets the inspected `letsramp/sample-microservices` demo system.

For live product catalog and cart routing:

```bash
set FRAMEWORK_PROFILE=real
set DEFAULT_SERVICE_BACKEND=stub
set PRODUCT_CATALOG_SERVICE_BACKEND=real
set CART_SERVICE_BACKEND=real
set CHECKOUT_SERVICE_BACKEND=stub
set PRODUCT_CATALOG_SERVICE_REAL_BASE_URL=http://localhost:60002
set CART_SERVICE_REAL_BASE_URL=http://localhost:60003
```

Then run the real-target-marked tests:

```bash
python -m pytest -q -m real_target
```

## Documentation

Key design and reference docs:

- [docs/target-architecture.md](C:/Users/Seguras/Downloads/cosas/ivo_personal/api-microservices-automation-framework/docs/target-architecture.md)
- [docs/service-layer-conventions.md](C:/Users/Seguras/Downloads/cosas/ivo_personal/api-microservices-automation-framework/docs/service-layer-conventions.md)
- [docs/fixture-strategy.md](C:/Users/Seguras/Downloads/cosas/ivo_personal/api-microservices-automation-framework/docs/fixture-strategy.md)
- [docs/real-target-onboarding-plan.md](C:/Users/Seguras/Downloads/cosas/ivo_personal/api-microservices-automation-framework/docs/real-target-onboarding-plan.md)
- [docs/real-target-service-mapping.md](C:/Users/Seguras/Downloads/cosas/ivo_personal/api-microservices-automation-framework/docs/real-target-service-mapping.md)

## Limitations

- checkout is still intentionally stubbed
- live real-target execution was prepared, but depends on an external runtime being available
- hybrid real product + real cart + stub checkout requires an explicit bridge test because stub checkout does not share state with the real cart service
- the framework currently focuses on a narrow backend flow, not broad product coverage

## Roadmap

Reasonable next steps if this project is continued:

1. run the real target reliably in local dev or CI
2. live-verify the real product catalog and cart paths
3. model the real checkout contract cleanly
4. add CI workflows for stub mode and optional real-target verification

## Portfolio Positioning

This repository is intentionally scoped to show:

- layered backend automation design
- documentation-first engineering discipline
- incremental legacy-to-clean-architecture translation
- honest handling of real-target integration risk
