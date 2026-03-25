# Real Target Service Mapping

## Inspected Target

Cloned and inspected:

- `C:\Users\Seguras\Downloads\cosas\real_targets\sample-microservices`

Key verified files used for mapping:

- `README.md`
- `src/docker-compose.yml`
- `src/variables.env`
- `src/productcatalogservice/rest.go`
- `src/cartservice/rest.go`
- `src/checkoutservice/rest.go`
- `api/openapi/rest.yaml`
- `skyramp/docker/demo/docker-compose.yml`
- `src/clients/rest/curl/checkout.sh`

## Framework To Target Mapping

### `product_catalog_service`

Framework service:

- `src/services/product_catalog_service/`

Real target service:

- `src/productcatalogservice/`

Verified REST endpoint:

- `GET /get-product?product_id=<id>`

Verified host mapping from exposed compose setup:

- `http://localhost:60002/get-product?product_id=<id>`

Current framework endpoint:

- `GET /products/{product_id}`

Payload difference:

- framework request builder currently assumes path-based id lookup
- real target expects the product id in a query parameter

Response difference:

- current stub returns product fields compatible with the framework model
- source contracts still describe `price_usd`
- live runtime verified on `2026-03-25` returned `priceUsd` and nested `currencyCode`
- framework normalization must tolerate both naming styles

Verified missing-product behavior:

- HTTP `404`
- no JSON error body is written by `src/productcatalogservice/rest.go`

Migration status:

- best first replacement candidate

### `cart_service`

Framework service:

- `src/services/cart_service/`

Real target service:

- `src/cartservice/`

Verified REST endpoints:

- `POST /cart/user_id/{user_id}`
- `GET /cart/user_id/{user_id}`
- `DELETE /cart/user_id/{user_id}`

Verified host mapping from exposed compose setup:

- `http://localhost:60003/cart/user_id/{user_id}`

Current framework endpoints:

- `POST /cart/user_id/{user_id}`
- `GET /cart/user_id/{user_id}`

Payload difference:

- current framework stub expects:
  - `{"item": {"product_id": "...", "quantity": 1}}`
- real target expects the raw cart item:
  - `{"product_id": "...", "quantity": 1}`

Response difference:

- current stub returns:
  - `{"status": "OK", "user_id": "...", "item": {...}}`
- real target returns:
  - `{"success": "200 OK"}`

Shared contract still usable:

- `GET /cart/user_id/{user_id}` returns cart state with `user_id` and `items`

Verified error behavior:

- empty user id on add/delete returns HTTP `403`
- invalid add payload returns HTTP `501`
- missing cart on get returns HTTP `404` with an error payload

Migration status:

- second replacement candidate after product catalog

### `checkout_service`

Framework service:

- `src/services/checkout_service/`

Real target service:

- `src/checkoutservice/`

Verified REST endpoint:

- `POST /checkout`

Verified host mapping from exposed compose setup:

- `http://localhost:60001/checkout`

Current framework endpoint:

- `POST /checkout/user_id/{user_id}`

Payload difference:

- current stub accepts a narrow payload:
  - `email`
  - `shipping_address`
  - user id in the path
- real target requires a larger order payload:
  - `user_id`
  - `user_currency`
  - `address`
  - `email`
  - `credit_card`

Response difference:

- current stub returns a simplified order object including:
  - `order_id`
  - `user_id`
  - `email`
  - `status`
  - flat item list
- real target returns `OrderResult` shaped around:
  - `order_id`
  - `shipping_tracking_id`
  - `shipping_cost`
  - `shipping_address`
  - `items`, where each item wraps a nested `item` object
- live runtime verified on `2026-03-25` omitted `zip_code` from `shipping_address`
- live runtime verified on `2026-03-25` also omitted per-item `cost`
- framework normalization must preserve the request zip code when the live response omits it

Dependency difference:

- current stub is self-contained
- real target checkout depends on cart, product catalog, currency, payment, email, and shipping services

Verified error behavior from source contract:

- malformed or incomplete request parsing can return HTTP `501`
- runtime failures in dependent downstream services can also surface as HTTP `501`

Live readiness note verified on `2026-03-25`:

- `POST /checkout` with `{}` returned HTTP `500` in the running compose environment even though a valid seeded checkout request succeeded with HTTP `200`
- framework readiness checks must treat that `500` as endpoint reachability, not as proof that valid checkout is broken
- live checkout also left the cart contents intact after a successful order; real-target integration assertions must not assume cart clearing

Migration status:

- real-target routing implemented in framework
- live runtime execution still environment-dependent

## Environment And Startup Requirements

Verified runtime requirements:

- source compose:
  - `src/docker-compose.yml`
  - starts the application, but does not expose the current service REST ports to the host
- service-internal REST ports:
  - `60000`
- service-internal gRPC/business ports:
  - cart `7070`
  - product catalog `3550`
  - checkout `5050`

Verified host-mapped demo compose:

- `skyramp/docker/demo/docker-compose.yml`
- host mappings:
  - checkout -> `http://localhost:60001`
  - product catalog -> `http://localhost:60002`
  - cart -> `http://localhost:60003`

## Narrowest Viable Real Flow

The target real flow implemented in the framework is:

1. real `product_catalog_service` lookup
2. real `cart_service` add/get
3. real `checkout_service` execution

Important runtime note:

- the real checkout path only works when the full dependency graph is up, not just the three exposed services

## Stub Replacement Order

Implemented in framework:

1. `product_catalog_service`
2. `cart_service`
3. `checkout_service`

## What Still Depends On Stubs

- deterministic local baseline
- local integration path independent of Docker/runtime availability

## Validation Note

Implementation wiring for real `product_catalog_service`, `cart_service`, and `checkout_service` was completed in the framework and the real-target test paths were executed.

Verified in this repository:

- stub mode remains green
- real-target mode resolves the verified `GET /get-product` contract when `product_catalog_service` is switched to `real`

Not verified live in this environment:

- a successful HTTP call to the real product catalog service, because no reachable runtime was available at `http://localhost:60002`

Implementation wiring for real `cart_service` was also completed in the framework and the real-target test path was executed.

Verified in this repository:

- stub mode remains green for cart, product catalog, checkout, and the existing integration baseline
- cart add-to-cart request and response differences are normalized behind the framework service layer
- checkout request and response differences are normalized behind the framework service layer
- a full real product -> cart -> checkout flow test exists in the suite

Not verified live in this environment:

- a successful HTTP call to the real cart service, because no reachable runtime was available at `http://localhost:60003`
- a successful HTTP call to the real checkout service, because no reachable runtime was available at `http://localhost:60001`
- a successful end-to-end real product/cart/checkout flow for the same reason
