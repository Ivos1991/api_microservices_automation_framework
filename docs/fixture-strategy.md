# Fixture Strategy

## Objective

Fixtures must stay explicit, composable, and local to the scenarios they support.

## Fixture Levels

### Root `conftest.py`

Keep only broadly shared infrastructure fixtures:

- settings
- stub-server lifecycle
- real-target readiness checks
- shared Allure hooks if needed

### Local `conftest.py`

Keep service- or integration-specific setup near the tests:

- request payload fixtures
- reusable scenario fixtures
- cleanup helpers

## Ownership Rules

- the fixture that creates state owns cleanup
- use function scope by default
- avoid hidden fixture coupling
- keep stateful environment preparation visible in the fixture list

## Example Local Fixture Ownership

### Cart service tests

- `cart_user_id`
- `cart_item_payload`
- `prepared_cart_with_item`

### Checkout integration tests

- `checkout_user_id`
- `checkout_address_payload`
- `prepared_cart_for_checkout`

## Teardown Philosophy

If the demo system exposes reset or cleanup APIs, use them.

If cleanup is not supported, prefer unique test data and idempotent scenario design over hidden cleanup hacks.
