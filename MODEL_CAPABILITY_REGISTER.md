# Model & Capability Register

Last updated: 2026-08-21
Status: Bootstrap skeleton; candidates require current verification and task-specific evaluation

## Purpose

Track candidate models by capability rather than brand and preserve evidence needed for routing qualification.

## Required fields

| Field | Description |
|---|---|
| capability_id | Canonical capability requested |
| model/provider | Current implementation candidate |
| version/date | Exact model/version or observation date |
| licence/terms | Commercial-use and deployment constraints where relevant |
| context | Context capability |
| tools/structured output | Required interface capabilities |
| quality evidence | Project-specific eval result |
| latency | Measured/reported latency |
| cost | Current price/cost basis |
| privacy/residency | Eligibility constraints |
| availability/rate limits | Operational constraints |
| status | WATCH / BENCHMARK / QUALIFIED / REJECT / RETIRE |
| replacement notes | Alternatives/fallbacks |

## Initial policy

- No model is universally preferred.
- No free model is routing-qualified solely because its price is zero.
- Frontier models should not be the default for every subtask.
- Open-weight/self-hosted candidates should remain in scope where suitable.
- Qualification must be task-specific and version-aware.

## Initial candidate capability classes

- low-risk classification/extraction
- bounded summarisation
- repository/code reconnaissance
- complex software reasoning
- runtime anomaly analysis
- instruction applicability analysis
- independent verification
- security-sensitive reasoning
- multimodal analysis where later required

No candidate is yet formally QUALIFIED.
