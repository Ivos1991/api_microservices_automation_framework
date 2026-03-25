# Coding Standards

## General

- prefer explicit behavior over hidden setup
- preserve the old repo layering style without carrying over its sprawl
- keep modules small and responsibility-driven
- keep names portfolio-safe and business-readable

## Naming

- service folders: `<domain>_service`
- service modules: `<domain>_service.py`
- endpoint modules: `<domain>_service_api.py`
- request builders: `<domain>_service_request.py`
- optional models: `<domain>_service_models.py`
- service tests: `tests/services_tests/<domain>_tests/test_<behavior>.py`
- integration tests: `tests/integration_tests/test_<behavior>_integration.py`

## Layer Boundaries

- request modules build payloads only
- service API modules build URLs and execute requests only
- service modules orchestrate request builders and APIs and perform only thin response validation
- tests hold business assertions and scenario meaning

## Fixtures

- keep root fixtures infrastructure-oriented
- prefer local `conftest.py` when a fixture belongs to one service domain or one integration flow
- the fixture that creates mutable state owns cleanup or reset

## Config

- expose configuration through a root `config` fixture
- keep the config manager environment-driven and intentionally small
- do not recreate the old repo's broad property surface unless the framework actually needs it

## Reporting

- Allure suite annotations belong in tests
- reusable attachments belong in `src/framework/reporting/`
- transport modules must not assemble scenario-level reporting

## Assertions

- prefer readable direct assertions in tests
- use custom helpers only when reuse is real and local to the framework
