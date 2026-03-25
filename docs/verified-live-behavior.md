# Verified Live Behavior

## Verification Date

- March 25, 2026

## Verified Runtime

Target repository:

- `C:\Users\Seguras\Downloads\cosas\real_targets\sample-microservices`

Compose command used:

```powershell
docker compose -f src/docker-compose.yml -f skyramp/docker/demo/docker-compose.yml up -d
```

## Verified Endpoints

### Product Catalog

- `GET http://localhost:60002/get-product?product_id=OLJCESPC7Z`
- returned HTTP `200`
- returned `priceUsd.currencyCode` in the live payload

### Cart

- `POST http://localhost:60003/cart/user_id/<user>`
- `GET http://localhost:60003/cart/user_id/<user>`
- add returned `{"success":"200 OK"}`
- get returned cart state with `user_id` and `items`

### Checkout

- `POST http://localhost:60001/checkout`
- valid seeded checkout request returned HTTP `200`
- empty readiness payload returned HTTP `500`
- live response omitted `zip_code` in `shipping_address`
- live response omitted per-item `cost`
- cart contents remained present after successful checkout

## Verified Test Result

Command:

```bash
python -m pytest -q -m real_target -p no:cacheprovider
```

Observed result:

- `5 passed`

## Why This Matters

The framework is normalized to the live runtime behavior that was actually observed, not only to the originally inspected source contracts.
