# Real Target Onboarding Plan

## Objective

Prepare the framework to support both:

- deterministic local stub execution
- incremental onboarding of the real microservices target

The current implementation must keep local stubs intact while allowing one service at a time to switch to the real target.

## Execution Modes

### Stub Mode

Purpose:

- fast local validation
- deterministic service and integration tests
- safe framework development without external runtime dependencies

Behavior:

- all services resolve to stub base URLs
- root `conftest.py` starts the local stub server
- existing service and integration tests stay fully local

### Real Target Mode

Purpose:

- verify real service contracts incrementally
- onboard one service slice at a time
- preserve the current framework architecture while replacing stubs selectively

Behavior:

- service base URLs resolve from explicit real-target configuration
- one service may point to the real target while others remain stubbed
- integration coverage should only compose real services that have already been validated

## Config Strategy

The framework now uses explicit env-driven routing:

- `FRAMEWORK_PROFILE=stub|real`
- `DEFAULT_SERVICE_BACKEND=stub|real`
- `PRODUCT_CATALOG_SERVICE_BACKEND=stub|real`
- `CART_SERVICE_BACKEND=stub|real`
- `CHECKOUT_SERVICE_BACKEND=stub|real`
- `*_SERVICE_STUB_BASE_URL`
- `*_SERVICE_REAL_BASE_URL`

Rules:

- stub remains the default profile
- each service can override the default backend independently
- if a service is configured for `real`, its real base URL must be explicitly provided

## Real Target Requirements To Configure

Before any service is switched to the real target, validate:

1. the target runtime is actually running
2. the required REST ports are reachable from the test runner
3. the selected service REST endpoint is stable enough for the current slice
4. the request and response contracts are mapped in the framework docs
5. downstream dependencies needed by that service are also reachable

## Verified Target Runtime Notes

From the inspected target repo:

- source repo: `C:\Users\Seguras\Downloads\cosas\real_targets\sample-microservices`
- default source compose file under `src/docker-compose.yml` does not publish the service REST ports to the host
- service REST handlers listen internally on port `60000`
- `skyramp/docker/demo/docker-compose.yml` provides host mappings for the three current candidate services:
  - checkout: `60001 -> 60000`
  - product catalog: `60002 -> 60000`
  - cart: `60003 -> 60000`

Implication:

- host-based framework execution cannot rely on `src/docker-compose.yml` alone
- the first real-target slice should use an execution setup that exposes REST ports to the runner

## Assumptions To Validate Before Switching A Service

### Product Catalog

- `GET /get-product?product_id=...` is reachable
- returned product contract matches the framework mapping
- product ids used by tests exist in the running catalog

### Cart

- `POST /cart/user_id/{user_id}` and `GET /cart/user_id/{user_id}` are reachable
- the real cart accepts the expected request body shape
- cart state is isolated enough for repeatable test users

### Checkout

- `POST /checkout` is reachable
- cart, product catalog, payment, shipping, currency, and email dependencies are all available
- request payload includes the required fields beyond the current stub slice

## Incremental Rollout Strategy

1. keep all current tests on stubs as the safety baseline
2. switch `product_catalog_service` first for a real-target service test
3. switch `cart_service` next after validating request/response differences
4. switch `checkout_service` last because it has the broadest downstream dependency set
5. only after service-level validation should the integration flow mix in real services

## Non-Goals For This Phase

- removing stubs
- full end-to-end migration to the real target
- broad new feature coverage
- hidden runtime setup inside fixtures
