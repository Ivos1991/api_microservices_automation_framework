# Testing Strategy

## Objective

Keep the repository small, explicit, and credible as a backend automation portfolio project.

## Test Layers

### Service Tests

Located under `tests/services_tests/`.

Purpose:

- validate one service slice at a time
- keep assertions close to the business operation
- use local fixtures for setup and teardown

Covered slices:

- product lookup
- add item to cart
- checkout seeded cart

### Integration Tests

Located under `tests/integration_tests/`.

Purpose:

- compose multiple services explicitly
- verify observable state and response transitions
- keep orchestration in the test body

Covered flows:

- stub product -> cart -> checkout baseline
- real product -> real cart -> real checkout
- real product + real cart + stub checkout bridge

## Execution Strategy

### Stub Baseline

Default regression safety net:

- deterministic
- local
- no Docker dependency

Recommended command:

```bash
python -m pytest -q -m "not real_target" -p no:cacheprovider
```

### Real-Target Verification

Use `real_target`-marked tests for live verification.

Rules:

- skip cleanly when the runtime is unreachable
- treat readiness-probe `500` responses carefully when the live target rejects empty payloads
- assert only verified live behavior
- do not present live verification as broader than it is

Recommended command:

```bash
python -m pytest -q -m real_target -p no:cacheprovider
```

## Assertion Philosophy

- keep business assertions in tests
- keep service-layer assertions transport-oriented and minimal
- normalize stub/real contract differences inside framework code
- align real-target assertions with observed runtime behavior, not assumed downstream side effects
