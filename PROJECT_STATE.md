# Project State — AI Runtime Intelligence OS

Last updated: 2026-08-22
Phase: Phase 0B — competitive boundary + experimental proof preparation
Status: B2 Baseline v1 frozen; Stage A attribution exhausted; Stage B native telemetry audit designed

## Current objective

Determine whether there is a durable commercial and technical opportunity for a provider-, model-, framework-, and gateway-agnostic AI runtime intelligence/control layer that improves outcome efficiency by allocating context, instructions, memory, tools, models, agents, reasoning effort, runtime, and verification according to task need, risk, and measured value.

## Governance baseline

- Central framework: `gurpreet-singh-au/ai-project-framework`
- Adopted baseline: v1.0.0
- Pinned commit: `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2`
- Adoption record: `PROJECT_STANDARD_ADOPTION.md`
- Project-specific constraints: `PROJECT_SPECIFIC_NON_NEGOTIABLES.md`
- Control maturity: Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise.

## What has been established

- Optimisation target is maximum useful outcome per unit compute subject to quality, risk, safety, privacy and governance constraints, not minimum tokens.
- Canonical runtime-resource model and provider-neutral telemetry model exist.
- Concrete benchmark cases B2-001, B3-001, B5-001 and B7-001 exist.
- Claude Code passive-observation harness is operational on Windows with benchmark-local Python 3.11.6, pytest 9.1.1 and `acceptEdits`.
- Deterministic B2 evaluator v1.1 independently verifies task success and mandatory compliance.
- Missing telemetry remains UNKNOWN rather than being coerced to zero.
- Runtime-specific observations must map through provider-neutral evidence rather than becoming architecture dependencies.

## B2 empirical baseline v1 — FROZEN

Included valid runs:

- `B2-001-baseline-r02`
- `B2-001-baseline-r03`
- `B2-001-baseline-r04`
- `B2-001-baseline-r05`
- `B2-001-baseline-r06`

Excluded:

- `B2-001-baseline-r01` — invalid harness/environment discovery run.

All five included runs passed the independent deterministic evaluator with `success: true` and `mandatory_compliance: true`.

Success rate: **5/5 = 100%**.

### Frozen descriptive distribution

| Metric | Mean | Median | Min | Max | Std dev | CV |
|---|---:|---:|---:|---:|---:|---:|
| Total cost USD | 0.19160122 | 0.19402950 | 0.17634690 | 0.20899400 | 0.01440126 | 7.52% |
| Duration ms | 21,774.4 | 21,977 | 19,175 | 24,032 | 2,139.66 | 9.83% |
| Fresh input tokens | 1,087.0 | 1,087 | 1,085 | 1,089 | 2.00 | 0.18% |
| Cached-input tokens | 297,513.4 | 299,675 | 261,376 | 335,910 | 35,235.14 | 11.84% |
| Cache-creation input tokens | 13,708.2 | 13,739 | 13,224 | 14,222 | 407.68 | 2.97% |
| Output tokens | 1,273.8 | 1,280 | 1,154 | 1,460 | 119.59 | 9.39% |
| Tool calls | 9.0 | 9 | 8 | 10 | 1.00 | 11.11% |

Formal record: `experiments/B2_BASELINE_V1_RESULT.md`.

No r07 is required before the first intervention unless later comparison variance shows n=5 was inadequate.

## B2-ATTR-001 Stage A — COMPLETE

Stage A exhausted existing Claude Code stream and local artifact evidence using:

- `experiments/analyze_b2_attribution_stage_a.py`
- `experiments/analyze_b2_native_usage_detail.py`

Formal result: `experiments/B2_ATTRIBUTION_STAGE_A_RESULT.md`.

### Important Stage A findings

1. **Spawned subagents are OBSERVED absent.** Every valid B2 run reports `subagent_stats.spawned = 0`, with zero requested/completed/failed subagents.
2. The repeated Haiku usage is therefore not evidence of a spawned subagent. Its exact internal purpose remains UNKNOWN.
3. Haiku usage is small and highly stable: approximately 1,069 input tokens, 13–14 output tokens, zero cache read/write and about USD 0.00113 per run.
4. Most observed cost/cache processing is associated with Sonnet.
5. Message-level usage snapshots show cache-read/context processing rising from roughly 22k early in a run to roughly 35k–36k later.
6. Final Sonnet cache-read totals of roughly 261k–336k are consistent with repeated processing/reuse across turns, not a unique 261k–336k context at one instant.
7. `usage.iterations` exists but is not proven to be a non-overlapping decomposition and is not summed with other usage objects.
8. Tool trajectories and visible tool-result volumes are observable, but exact per-request retention/compaction is not.

### Stage A decision

**INSUFFICIENT EVIDENCE FOR COMPOSITION ATTRIBUTION.**

Native stream evidence cannot distinguish system instructions, project instructions, task prompt, tool schemas, repository/file content, accumulated history and residual provider/runtime overhead well enough to choose an optimisation intervention.

H1/H2 remain unresolved. H3 has not been tested.

## B2-ATTR-001 Stage B — DESIGNED

Plan: `experiments/B2_ATTRIBUTION_STAGE_B_PLAN.md`.

Anthropic documentation confirms OpenTelemetry is a supported Claude Code monitoring mechanism, but that alone does not establish that its payload resolves prompt/context composition. Stage B therefore starts with a **native OpenTelemetry capability audit** rather than immediately modifying the benchmark harness or adding a proxy/SDK.

Stage B sequence:

1. discover the telemetry signals actually available in the installed Claude Code version;
2. classify useful fields as OBSERVED/DERIVED/UNAVAILABLE/UNKNOWN;
3. if useful, run one diagnostic-only telemetry-enabled B2 capture;
4. measure instrumentation overhead/semantic differences;
5. only then decide whether native telemetry is sufficient or escalation to a thin wrapper is justified.

Do not compare a first telemetry-enabled diagnostic run directly against frozen Baseline v1 as a savings claim.

## Naturalistic observation lane

`NAT-001` used a fresh Claude Cowork session against a GitHub clone and independently recommended context/instruction composition attribution after the B2 baseline. Treat it as naturalistic analytical evidence only.

## Cross-runtime lane — Codex

Codex is now useful as a separate controlled runtime/provider lane. Prepare a dedicated adapter and reuse the same B2 task semantics and independent evaluator where technically compatible.

Do not mix Codex observations into Claude B2 Baseline v1. Runtime-specific telemetry remains separate and maps into the canonical provider-neutral schema.

The Codex lane is a cross-runtime validation test of the provider-agnostic thesis, not a substitute for completing Claude Stage B.

## Current differentiation hypotheses to prove

1. Task Resource Profiling can estimate useful resource requirements before execution.
2. Instruction Applicability Compilation can reduce instruction load without governance regression.
3. Context Utility Allocation can reduce stale/duplicate context while preserving evidence and outcome quality.
4. Agent Spawn Economics can decide whether another subagent is justified before paying for it.
5. Marginal Compute Utility can compare the value of additional context, reasoning, agents, searches, tools and verification.
6. Useful State Change / Loop Intelligence can identify low-progress runtime trajectories earlier than generic tracing alone.
7. Execution Counterfactuals can identify which resources contributed materially to success.
8. Outcome-Conditioned Policy Learning can learn task fingerprint -> execution strategy mappings across providers and runtimes.

## First empirical milestone

> On at least two representative workloads, demonstrate material compute/cost or latency reduction while maintaining non-inferior parent-task quality and 100% tested mandatory-rule compliance.

The thesis is not yet validated.

## Current blockers / unknowns

- Exact request composition remains unresolved in Claude Code.
- Native OpenTelemetry field coverage for the installed runtime has not yet been locally verified.
- Secondary Haiku invocation purpose remains UNKNOWN.
- Tool-schema contribution and exact conversation/tool-result retention remain unresolved.
- Useful State Change and no-progress intervals remain unmeasured.
- Instrumentation overhead remains unknown.
- Cross-runtime behavior has not yet been measured with Codex.
- Customer willingness to pay remains unproven.

## Immediate next work

1. Keep Claude B2 Baseline v1 frozen at r02-r06.
2. Execute Stage B1 native OpenTelemetry capability discovery before changing benchmark semantics.
3. If B1 provides useful signals, create one separate diagnostic run `B2-ATTR-001-otel-diagnostic-r01`; do not treat it as a baseline/intervention run.
4. Keep any prompt/code-bearing raw telemetry local and out of Git.
5. Prepare a separate Codex controlled-baseline adapter in parallel, reusing canonical B2 semantics and deterministic evaluation where technically compatible.
6. Do not select a context/instruction optimisation intervention until attribution evidence justifies one.
7. Do not build a production control plane yet.
