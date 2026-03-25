# Real Runtime Setup

## Objective

Bring up the selected real microservices target locally so the framework can execute live REST calls against:

- product catalog
- cart
- checkout

without removing the existing stub mode.

## Prerequisites

- Docker Desktop or Docker Engine with Docker Compose v2
- network access to pull the required images
- the target repo cloned at:
  - `C:\Users\Seguras\Downloads\cosas\real_targets\sample-microservices`

## Verified Runtime Layout

Base stack:

- `src/docker-compose.yml`

Host-port exposure override:

- `skyramp/docker/demo/docker-compose.yml`

Why both are needed:

- the base compose file brings up the full dependency graph required by checkout
- the override exposes product catalog, cart, and checkout REST ports to the host runner

## Startup Commands

From the cloned target repo root:

```bash
cd C:\Users\Seguras\Downloads\cosas\real_targets\sample-microservices
docker compose -f src/docker-compose.yml -f skyramp/docker/demo/docker-compose.yml up -d
```

To stop the runtime:

```bash
docker compose -f src/docker-compose.yml -f skyramp/docker/demo/docker-compose.yml down
```

## Exposed Host Ports

- product catalog: `http://localhost:60002`
- cart: `http://localhost:60003`
- checkout: `http://localhost:60001`

## Framework Environment Variables

The framework can use the default real URLs already reflected in `.env.example`:

- `PRODUCT_CATALOG_SERVICE_REAL_BASE_URL=http://localhost:60002`
- `CART_SERVICE_REAL_BASE_URL=http://localhost:60003`
- `CHECKOUT_SERVICE_REAL_BASE_URL=http://localhost:60001`

Example real-mode switching:

```bash
set FRAMEWORK_PROFILE=real
set DEFAULT_SERVICE_BACKEND=stub
set PRODUCT_CATALOG_SERVICE_BACKEND=real
set CART_SERVICE_BACKEND=real
set CHECKOUT_SERVICE_BACKEND=real
```

## Verification Steps

### Product Catalog

```bash
curl "http://localhost:60002/get-product?product_id=OLJCESPC7Z"
```

Expected:

- HTTP `200`
- product JSON with `id`, `name`, `description`, `picture`, and pricing data
- live runtime verified on `2026-03-25` returned `priceUsd.currencyCode`

### Cart

```bash
curl -X POST "http://localhost:60003/cart/user_id/abcde" ^
  -H "content-type: application/json" ^
  -d "{\"product_id\":\"OLJCESPC7Z\",\"quantity\":1}"
```

```bash
curl "http://localhost:60003/cart/user_id/abcde"
```

Expected:

- add returns `{"success":"200 OK"}`
- get returns `{"user_id":"abcde","items":[...]}`

### Checkout

```bash
curl -X POST "http://localhost:60001/checkout" ^
  -H "content-type: application/json" ^
  -d "{\"user_id\":\"abcde\",\"user_currency\":\"USD\",\"address\":{\"street_address\":\"1600 Amp street\",\"city\":\"Mountain View\",\"state\":\"CA\",\"country\":\"USA\",\"zip_code\":\"94043\"},\"email\":\"someone@example.com\",\"credit_card\":{\"credit_card_number\":\"4432-8015-6251-0454\",\"credit_card_cvv\":672,\"credit_card_expiration_year\":24,\"credit_card_expiration_month\":1}}"
```

Expected:

- HTTP `200`
- JSON order result with `order_id`, `shipping_tracking_id`, `shipping_cost`, `shipping_address`, and `items`
- live runtime verified on `2026-03-25` omitted `zip_code` from the response shipping address
- live runtime verified on `2026-03-25` omitted per-item `cost`

## Verified Status

Verified on `2026-03-25`:

- Docker runtime started successfully
- product catalog endpoint reachable on `60002`
- cart endpoint reachable on `60003`
- checkout endpoint reachable on `60001`
- real-target pytest selection passed in this repository

## Known Issues And Limitations

- checkout depends on the full base stack; the exposed-port override is not sufficient by itself
- real-target tests in this repository skip cleanly when the runtime is unreachable
- `POST /checkout` with an empty payload may return HTTP `500` even while valid checkout requests succeed
