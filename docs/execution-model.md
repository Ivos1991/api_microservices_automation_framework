# Execution Model

## Objective

Describe how the same framework architecture supports both deterministic local execution and live-target verification.

## Shared Principle

Service modules do not change between execution modes. Configuration decides which backend each service uses.

## Stub Mode

Purpose:

- deterministic local regression coverage
- framework development without Docker
- fast portfolio-safe demonstrations

Behavior:

- root `conftest.py` starts the local fake runtime
- all services resolve to stub base URLs
- tests execute without external dependencies

## Real-Target Mode

Purpose:

- live contract verification against the sample microservices runtime
- per-service backend switching without changing test structure

Behavior:

- service backends are selected through environment variables
- product catalog, cart, and checkout can point to the live runtime independently
- readiness checks skip cleanly when the target is unavailable

## Hybrid Usage

Hybrid execution is still supported when needed.

Example:

- real product catalog
- real cart
- stub checkout

Important limitation:

- stub and real runtimes do not share state automatically
- when a hybrid scenario needs data to cross that boundary, the test must bridge the state explicitly

## Config Surface

Key variables:

- `FRAMEWORK_PROFILE`
- `DEFAULT_SERVICE_BACKEND`
- `PRODUCT_CATALOG_SERVICE_BACKEND`
- `CART_SERVICE_BACKEND`
- `CHECKOUT_SERVICE_BACKEND`
- service-specific stub and real base URLs

## Verified Live Ports

- product catalog: `http://localhost:60002`
- cart: `http://localhost:60003`
- checkout: `http://localhost:60001`
