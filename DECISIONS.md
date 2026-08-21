# Decisions — AI Runtime Intelligence OS

Last updated: 2026-08-21

## D-001 — Treat this as a serious research project

**Decision:** Proceed with deep research and structured experiments before production coding.

**Reason:** The problem appears broad and potentially durable, but the commercial opportunity and intervention feasibility remain unproven.

**Status:** Accepted

## D-002 — Use `ai-runtime-intelligence-os` as the working repository/product name

**Decision:** Use AI Runtime Intelligence OS as the working project identity.

**Reason:** It is broader and more durable than a context-only or token-optimisation name.

**Status:** Accepted; naming can be revisited after market validation.

## D-003 — GitHub is the engineering/research source of truth

**Decision:** Important research, evidence, state, decisions, experiments, and architecture must be recorded in the repository.

**Status:** Accepted

## D-004 — Adopt the central AI Project Framework

**Decision:** Pin `gurpreet-singh-au/ai-project-framework` v1.0.0 at commit `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2`.

**Reason:** Avoid duplicate or drifting governance and preserve cross-project continuity.

**Status:** Accepted

## D-005 — Keep project-specific non-negotiables separate from universal standards

**Decision:** Use `PROJECT_SPECIFIC_NON_NEGOTIABLES.md` only for rules unique to this project; do not duplicate the universal framework.

**Status:** Accepted

## D-006 — Optimise outcomes, not tokens

**Decision:** The core optimisation objective is quality-/risk-constrained runtime efficiency, not minimum token consumption or minimum spend.

**Status:** Accepted

## D-007 — Treat instructions as a first-class runtime resource

**Decision:** Research Instruction Intelligence as a distinct engine alongside context, memory, tools, models, agents, runtime, and verification.

**Status:** Accepted

## D-008 — Treat subagent spawning as an economic/resource-allocation decision

**Decision:** Do not assume more agents improve outcomes. Measure marginal contribution, overlap, cost, diversity, and coordination overhead.

**Status:** Accepted

## D-009 — OpenRouter is an adapter, not a foundation

**Decision:** OpenRouter may be used for experimentation and routing, including free/cheap model lanes, but canonical routing intelligence must remain within our architecture.

**Status:** Accepted

## D-010 — Observe before autonomous intervention

**Decision:** Initial product/prototype progression is `Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise`.

**Reason:** Autonomous pruning, model switching, and agent termination require evidence that quality and governance are preserved.

**Status:** Accepted

## D-011 — Deterministic software controls mandatory constraints

**Decision:** Budgets, permissions, stop conditions, mandatory policy, provenance, schema validation, and equivalent hard constraints should be deterministically enforced where feasible.

**Status:** Accepted

## Pending decisions

- First commercial/customer wedge.
- First supported runtime/provider adapter.
- Telemetry storage/observability stack.
- Evaluation harness and benchmark corpus.
- Prototype implementation stack.
- Whether to include self-hosted/open-weight inference in the first experimental milestone.
