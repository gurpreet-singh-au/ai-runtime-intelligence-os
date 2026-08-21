# Infrastructure Strategy — AI Runtime Intelligence OS

Last updated: 2026-08-21
Status: Research/prototype stage; no production infrastructure approved

## Current posture

Do not provision significant paid infrastructure yet. Phase 0 should favour low-cost/local/reusable tools until telemetry, workload, security, and commercial requirements are clearer.

## Requirements to determine before staging

- expected execution volume and concurrency
- trace/event volume
- retention requirements
- sensitive-data classification
- regional/data-residency needs
- model/provider traffic patterns
- background evaluation workloads
- storage requirements for evidence and traces
- dashboard/query latency needs
- backup/recovery expectations
- tenancy/isolation model
- cost ceilings

## Architecture principles

- Keep provider-specific code at adapter boundaries.
- Prefer portable canonical schemas and exportable telemetry.
- Separate hot runtime state from immutable/retrievable evidence.
- Avoid making a gateway, observability vendor, or agent framework the sole owner of canonical state.
- Reuse portfolio infrastructure where appropriate before purchasing new services.
- Compare managed, open-source/self-hosted, and direct-provider approaches using TCO, not headline price.

## Likely infrastructure domains

1. Runtime telemetry ingestion
2. Canonical event/state database
3. Evidence/trace object storage
4. Evaluation/benchmark runner
5. Model/provider gateway adapters
6. Dashboard/query service
7. Policy/configuration service
8. Secrets and credential management
9. Queue/background execution
10. Observability/alerting

## Current decisions

- No cloud provider selected.
- No database selected.
- No observability vendor selected.
- No model gateway made foundational.
- OpenRouter may be benchmarked as an adapter.
- OpenTelemetry should be evaluated as a portability mechanism.

## Pre-staging gate

Before paid staging, re-evaluate current managed and open-source options using the central framework's infrastructure governance standard and record a Stay / Optimise / Consolidate / Migrate-style decision with current evidence.
