# Reporting And CI

## Reporting

Allure is the reporting solution for this repository.

### Reporting Principles

- Allure annotations belong in tests
- reusable attachment formatting belongs in the framework reporting layer
- services and service APIs must not own scenario-level reporting logic
- technical request/response diagnostics may exist in the base execution layer if useful and controlled

### Planned Reporting Helpers

- attach structured JSON snapshots
- attach request/response summaries
- attach integration before/after state snapshots

## CI/CD Direction

The first CI target should remain simple:

- install Python dependencies
- run the stub-mode service tests
- run the stub-mode integration tests
- optionally run real-target-marked tests only when the target runtime is available
- publish Allure results as artifacts

## Initial Workflow Shape

- PR validation workflow
- manual workflow with selectable pytest target and markers

Do not over-design CI in the first phase.

## GitHub Workflow Shape

The repository can now support a small workflow set:

- PR validation running the stub-only suite
- manual dispatch with selectable execution mode
- scheduled nightly regression running the full suite

The reusable workflow should:

- install Python dependencies from `requirements.txt`
- patch known-broken upstream runtime files after checkout when Docker base images disappear upstream
- start the sample microservices Docker runtime only when real-target execution is requested
- pin the external `letsramp/sample-microservices` checkout to a known-good commit instead of floating on upstream `main`
- run pytest with the requested marker selection
- upload Allure results as artifacts

## Real-Runtime Stability Notes

The nightly workflow depends on an external checked-out runtime:

- `letsramp/sample-microservices`

That dependency is not stable enough to treat as immutable infrastructure:

- upstream Dockerfiles can reference base images that later disappear from Docker Hub
- those failures happen before pytest starts and are not framework-code regressions

Current guarded CI hotfix:

- replace every `FROM openjdk:8-slim` line in `src/adservice/Dockerfile`
- with `FROM eclipse-temurin:8-jdk-jammy`
- fail the patch step if any `openjdk:8-slim` reference remains before `docker compose up -d`

Reason for the hotfix:

- Docker Hub no longer resolves `openjdk:8-slim`
- nightly real-target startup otherwise fails during the `adservice` image build stage

## Publishing Note

The CI design remains intentionally small:

- stub mode is the default PR safety net
- real-target mode is available for manual and scheduled verification
- the workflow layer mirrors the repository execution model instead of inventing new test types
