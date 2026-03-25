# Implementation Plan

## Current Implementation Goal

Preserve the implemented hybrid architecture in a portfolio-ready state without adding further service slices.

## Implemented Slices

### Service Domain

1. `cart_service`
2. `product_catalog_service`
3. `checkout_service`

### First Service Test

- add item to cart returns an OK status and echoes the added item contract

### Current Integration Coverage

- retrieve a valid product
- add the product to cart
- checkout the cart
- verify the returned order contains the expected item and user

- real-target-aware product lookup path
- real-target-aware cart path
- hybrid real product + real cart + stub checkout bridge path

## Current Status

Completed:

1. old repo reference audit
2. planning-doc alignment
3. framework scaffold
4. config manager and base API executor
5. service slices for product catalog, cart, and checkout
6. deterministic stub-mode service and integration tests
7. incremental real-target routing for product catalog and cart
8. portfolio-ready hybrid mode preparation

## Intentionally Out Of Scope

- UI or browser automation
- broad multi-service coverage
- direct database assertions
- CI workflow implementation beyond planning
- deep contract-test infrastructure
