# Hybrid Mode Design

## Objective

Allow the framework to mix stubbed and real services without changing service boundaries.

## Core Rule

Service modules do not know whether they are speaking to a stub or the real target beyond config-driven route and payload differences owned by the service/API/request layers.

## How Routing Works

Routing is controlled through:

- `FRAMEWORK_PROFILE`
- `DEFAULT_SERVICE_BACKEND`
- per-service backend overrides
- per-service stub and real base URLs

Example:

- real `product_catalog_service`
- real `cart_service`
- stub `checkout_service`

## Why Hybrid Mode Exists

- preserves deterministic local development
- allows safe incremental onboarding of real contracts
- keeps unfinished services stubbed instead of forcing premature migration

## Important Limitation

Hybrid mode does not magically create shared state across runtimes.

Example:

- a stubbed `checkout_service` cannot directly consume state stored in a real `cart_service`

When that gap matters, tests must use an explicit bridge and must document that bridge clearly. Hidden synchronization would make the framework less honest and harder to reason about.
