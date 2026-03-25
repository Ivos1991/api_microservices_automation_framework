# Known Limitations

## Scope

- The repository intentionally implements only three service slices.
- The framework validates one narrow backend flow instead of broad product coverage.

## Runtime Behavior

- Real-target execution depends on the external sample microservices runtime being available locally.
- The running checkout service can return HTTP `500` for an empty readiness payload even when valid checkout requests succeed.
- The live checkout response may omit fields that older source contracts imply, such as `zip_code` or per-item `cost`.
- The live checkout flow does not clear cart contents after a successful order.

## Test Strategy

- Real-target tests are verification tests, not full contract-test coverage.
- Stub mode remains the deterministic safety baseline.
- No direct database assertions are included.

## Project Boundaries

- No UI automation
- No CI workflow implementation in this repository
- No additional service expansion beyond product catalog, cart, and checkout
