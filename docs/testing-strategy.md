# Testing Strategy

## Objective

Keep the framework test pyramid small, explicit, and credible.

## Test Layers

### Service Tests

Located under `tests/services_tests/`.

Purpose:

- validate one service slice at a time
- keep assertions close to the business operation
- avoid cross-service coupling unless the fixture explicitly prepares it

Current examples:

- product lookup
- add item to cart
- checkout seeded cart

### Integration Tests

Located under `tests/integration_tests/`.

Purpose:

- compose multiple services explicitly
- validate observable state transitions
- keep orchestration in the test, not hidden in service modules

Current examples:

- all-stub product -> cart -> checkout baseline
- real product + real cart + stub checkout bridge path

## Execution Strategy

### Stub Baseline

Always keep the deterministic stub suite green.

Why:

- it is the regression safety net
- it proves the framework architecture without external runtime dependencies

### Real-Target Tests

Use `real_target`-marked tests for live verification.

Rules:

- skip cleanly when the runtime is unreachable
- do not overstate live verification
- onboard one service at a time

## Assertion Philosophy

- keep business assertions in tests
- keep service-layer assertions transport-oriented and minimal
- normalize contract differences inside framework code when it improves test readability
