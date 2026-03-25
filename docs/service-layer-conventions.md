# Service Layer Conventions

## Objective

Standardize the service-oriented API structure while preserving the old repo hierarchy style.

## 1. `name_service.py`

Responsibilities:

- expose the domain-facing functions used by tests
- orchestrate request building and API execution
- perform basic transport-success validation
- return parsed JSON or small typed models

Examples:

- `add_item_to_cart(...)`
- `get_cart(...)`

Must not:

- build endpoint URLs inline
- own raw HTTP execution behavior
- contain scenario-level Allure reporting

## 2. `name_service_api.py`

Responsibilities:

- define one thin method per endpoint
- construct endpoint URLs
- call the shared base API executor
- remain transport-focused

Examples:

- `post_add_item(...)`
- `get_cart(...)`

Must not:

- perform business assertions
- build rich request payloads from many fields
- infer scenario meaning

## 3. `name_service_request.py`

Responsibilities:

- build request dictionaries and query params
- translate typed request models into API payloads
- keep payload construction reusable and testable

Examples:

- `build_add_item_payload(...)`

Must not:

- execute HTTP calls
- assert API behavior

## 4. Optional `name_service_models.py`

Use only when the slice benefits from typed contracts:

- request objects passed into the service layer
- small response objects returned by services
- fixture-driven data objects

Skip the file when raw dictionaries are genuinely clearer for the slice.

## 5. Tests

Tests should:

- call service-layer functions, not raw API methods
- keep business assertions in the test body
- use Allure parent suite, suite, and sub suite annotations
- use local fixtures for scenario setup and teardown

## 6. Fixtures And Config

Fixtures should:

- keep setup visible
- own cleanup where they create mutable state
- stay local when tied to one service domain or one integration flow

Config should:

- be exposed through a root `config` fixture
- resolve service base URLs, environment name, timeouts, and reporting toggles
- stay framework-owned and environment-driven

## 7. Base API Layer

The shared base API layer should own:

- HTTP execution
- timeout handling
- optional retries
- controlled request/response diagnostics

It must not own business assertions or service-specific payload knowledge.
