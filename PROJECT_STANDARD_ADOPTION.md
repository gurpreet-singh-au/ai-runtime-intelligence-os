# Project Standards Adoption Record

## Project

**Name:** AI Runtime Intelligence OS  
**Repository:** `gurpreet-singh-au/ai-runtime-intelligence-os`  
**Date adopted:** 2026-08-21  
**Framework repository:** `gurpreet-singh-au/ai-project-framework`  
**Framework baseline:** v1.0.0  
**Pinned framework commit:** `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2`

## Governing hierarchy

1. `ai-project-framework/UNIVERSAL_PROJECT_NON_NEGOTIABLES.md`
2. Reusable standards explicitly adopted below
3. `PROJECT_SPECIFIC_NON_NEGOTIABLES.md`
4. Architecture decisions / `DECISIONS.md`
5. Research, implementation documentation, code and infrastructure

The central framework remains canonical. Future framework changes are not silently inherited; they require reassessment and an explicit update to this record.

## Mandatory framework documents reviewed

- `UNIVERSAL_PROJECT_NON_NEGOTIABLES.md` — ADOPT
- `PROJECT_BOOTSTRAP.md` — ADOPT
- `PROJECT_LIFECYCLE.md` — ADOPT
- `BOOTSTRAP_DISTRIBUTION.md` — ADOPT
- `INFRASTRUCTURE_GOVERNANCE.md` — ADOPT
- `BUILD_REUSE_INTEGRATE.md` — ADOPT

## Reusable standards

- `MODEL_AGNOSTIC_STANDARD.md` — **ADOPT**
  - Central to provider/model/gateway independence and dynamic routing.
- `OPEN_SOURCE_GOVERNANCE_STANDARD.md` — **ADOPT**
  - Required because open-weight models, gateways, telemetry stacks and agent/runtime frameworks will be evaluated continuously.
- `CAPABILITY_CONTRACT_STANDARD.md` — **ADOPT**
  - Runtime decisions must be capability-driven rather than vendor-driven.
- `ADAPTER_ARCHITECTURE_STANDARD.md` — **ADOPT**
  - Providers, gateways, agent runtimes and observability systems must remain replaceable.
- `CANONICAL_DATA_OWNERSHIP_STANDARD.md` — **ADOPT**
  - Runtime policy, telemetry, evaluations, routing decisions and evidence must remain ours.
- `SELF_IMPROVEMENT_GOVERNANCE.md` — **ADOPT**
  - The system is intended to learn from measured outcomes but must not self-mutate protected controls.
- `AGENT_GOVERNANCE_STANDARD.md` — **ADOPT**
  - Agent/subagent spawning, authority, budgets, tools and autonomy are first-class concerns.
- `EVALUATION_AND_OBSERVABILITY_STANDARD.md` — **ADOPT**
  - The opportunity depends on proving quality-preserving efficiency improvements with representative evaluations.
- `DEPENDENCY_EXIT_AND_LIFECYCLE_STANDARD.md` — **ADOPT**
  - Model/provider/gateway/framework churn is expected and must be planned for.
- `INFRASTRUCTURE_GOVERNANCE.md` — **ADOPT**
  - Serving, inference, observability and storage choices must be reassessed based on TCO and portability.
- `BUILD_REUSE_INTEGRATE.md` — **ADOPT**
  - Existing routing, telemetry, evaluation and orchestration components should be reused/integrated before custom-building.

## Project-specific additions

See `PROJECT_SPECIFIC_NON_NEGOTIABLES.md`.

## Current deviations

None approved.

## Review triggers

Reassess this adoption record after:

- material change to the central framework;
- major architecture decision;
- first runtime prototype;
- first external provider/gateway integration;
- first autonomous intervention capability;
- pre-staging review;
- major provider/model/pricing change;
- commercial pivot;
- material security/privacy finding.

## Next reassessment

At the first formal architecture/prototype gate or when a newer framework release is proposed for adoption, whichever comes first.
