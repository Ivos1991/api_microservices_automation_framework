# Target System Analysis

## Chosen Target

- `letsramp/sample-microservices`

Reference sources used during planning:

- https://github.com/letsramp/sample-microservices
- https://github.com/GoogleCloudPlatform/microservices-demo

## Why This Target

This target is a better fit than a UI-first demo because it is explicitly microservices-based and exposes REST traffic in addition to gRPC and Thrift.

That makes it suitable for an API-first automation framework with clean service-level modules.

## Observed Service Landscape

The target inherits the Online Boutique service model and exposes REST support for microservices such as:

- `cartservice`
- `checkoutservice`
- `productcatalogservice`
- `currencyservice`
- `paymentservice`
- `shippingservice`
- `emailservice`
- `recommendationservice`
- `adservice`

## Observed Data Stores And State

From the target documentation and inherited Online Boutique architecture:

- `cartservice` persists cart state in Redis
- `productcatalogservice` serves product data from a static catalog source
- checkout-related services are largely orchestration and mocked downstream behavior
- some downstream state is returned in API responses rather than exposed through a queryable database

Implication for the framework:

- integration validation should primarily use multi-step API behavior and returned state
- persisted-state assertions are practical where the target exposes observable state, especially cart retrieval after mutation
- the first implementation should not assume direct database assertions across all services

## Confirmed Example REST Behavior

Documented examples include:

- add item to cart
  - `POST /cart/user_id/{user_id}`
- get cart
  - `GET /cart/user_id/{user_id}`
- checkout flow returning order details
  - documented in the demo test examples with an order payload containing `order_id`, shipping details, and item data

## Candidate First Business Flows

### Best First Slice

1. list or source a valid product id
2. add item to cart
3. fetch cart
4. checkout
5. verify returned order contents

Why this is best:

- clear multi-service behavior
- API-first
- observable state before and after mutation
- portfolio-safe and understandable

### Secondary Candidate Slice

- add multiple products to cart
- verify cart quantity aggregation
- checkout and verify multi-item order payload

### Later Candidate Slice

- recommendation or ads behavior tied to cart contents
- use only after the core cart and checkout layer is stable
