# AGENTS.md

## Purpose

This repository is planned as an API-first microservices automation framework.

The workflow for this repository is documentation-first:

1. inspect the current target system and reference material
2. update the planning docs in `docs/`
3. confirm the intended architecture and slice boundaries
4. implement only after the relevant docs exist and match the intended change
5. keep docs aligned with the code after each meaningful phase

## Architecture Rules

- keep service orchestration in `*_service.py`
- keep endpoint execution in `*_service_api.py`
- keep request-body construction in `*_service_request.py`
- keep test assertions in tests, not in API transport modules
- keep Allure reporting reusable and framework-owned
- keep fixtures explicit, local, and teardown-aware
- preserve a clear distinction between service tests and integration tests

## Planning Rules

Before implementation, the repository must maintain these planning docs:

- `docs/current-reference-analysis.md`
- `docs/reusable-patterns.md`
- `docs/target-architecture.md`
- `docs/fixture-strategy.md`
- `docs/reporting-and-ci.md`
- `docs/implementation-plan.md`
- `docs/coding-standards.md`
- `docs/service-layer-conventions.md`

## Design Principles

- readability over cleverness
- explicit behavior over hidden setup
- modularity without abstraction sprawl
- reusable technical helpers only when duplication is real
- portfolio-safe naming, structure, and reporting
