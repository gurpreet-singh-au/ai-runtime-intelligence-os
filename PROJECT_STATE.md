# Project State — AI Runtime Intelligence OS

Last updated: 2026-08-22
Phase: Phase 0B — competitive boundary + experimental proof preparation
Status: First B2 empirical baseline series frozen; attribution experiment designed

## Current objective

Determine whether there is a durable commercial and technical opportunity for a provider-, model-, framework-, and gateway-agnostic AI runtime intelligence/control layer that improves outcome efficiency by allocating context, instructions, memory, tools, models, agents, reasoning effort, runtime, and verification according to task need, risk, and measured value.

## Governance baseline

- Central framework: `gurpreet-singh-au/ai-project-framework`
- Adopted baseline: v1.0.0
- Pinned commit: `8128f2d9b91cec1ec2e9f73833be32cbf01cfdf2`
- Adoption record: `PROJECT_STANDARD_ADOPTION.md`
- Project-specific constraints: `PROJECT_SPECIFIC_NON_NEGOTIABLES.md`

## What has been established

- Core thesis: optimisation target is not minimum tokens; it is maximum useful outcome per unit of computation subject to quality, risk, safety, privacy, and governance constraints.
- Runtime resource classes defined in `architecture/AI_RUNTIME_RESOURCE_MODEL.md`.
- Instruction Intelligence identified as a first-class subsystem.
- Agent/subagent economics identified as a first-class subsystem.
- OpenRouter identified as a useful replaceable routing/gateway adapter, not a canonical dependency.
- Competitive/adjacent landscape documented in `research/MARKET_LANDSCAPE.md` and `research/COMPETITOR_MATRIX.md`.
- Canonical provider-neutral telemetry model defined in `architecture/TELEMETRY_MODEL.md`.
- Benchmark and baseline experiment design defined in `research/BENCHMARK_AND_BASELINE_SPEC.md`.
- Machine-readable experiment run schema defined in `experiments/RUN_SCHEMA.json`.
- Concrete benchmark cases B2-001, B3-001, B5-001 and B7-001 defined in `benchmarks/README.md`.
- Claude Code passive-observation harness created under `experiments/adapters/claude_code/`.
- Windows harness uses a benchmark-local Python 3.11 virtual environment, pinned pytest 9.1.1 and Claude Code `acceptEdits`.
- Deterministic B2 finalization is wired into the runner via `finalize_b2_outcome.py`; evaluator v1.1 correctly parses changed paths.
- `experiments/TELEMETRY_GAP_DECISION_PROTOCOL.md` governs whether additional telemetry is justified by a specific hypothesis.
- `experiments/analyze_b2_baselines.py` aggregates valid local B2 runs into descriptive baseline statistics.
- Control maturity path remains: Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise.

## B2 empirical baseline v1 — FROZEN

Included valid runs:

- `B2-001-baseline-r02`
- `B2-001-baseline-r03`
- `B2-001-baseline-r04`
- `B2-001-baseline-r05`
- `B2-001-baseline-r06`

Excluded:

- `B2-001-baseline-r01` — invalid discovery run; harness/environment evidence only.

All five included runs passed the independent deterministic evaluator with `success: true` and `mandatory_compliance: true`.

Success rate across included runs: **5/5 = 100%**.

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

Observed models in every valid run:

- `claude-sonnet-5`
- `claude-haiku-4-5-20251001`

Native CLI telemetry completeness remains 0.4667 under the generic rubric. Missing fields remain UNKNOWN, not zero.

Formal result: `experiments/B2_BASELINE_V1_RESULT.md`.

## Baseline interpretation

- Fresh task input is extremely stable, while cached-input processing, tool calls, duration, output and cost vary materially more.
- This establishes runtime variance and a resource-profile signal, but does not establish causality.
- Provider-reported cached-input tokens are processed/cache usage and must not be treated as unique semantic context size.
- No r07 is required before the first attribution/intervention phase unless later comparison variance shows n=5 was inadequate.

## Naturalistic observation lane

`NAT-001` used a fresh Claude Cowork session against a GitHub clone of this repository and asked for the highest-value next experiment without modifying the repo. Its independent recommendation was to investigate context/instruction composition after the B2 baseline series. Treat this as naturalistic analytical evidence only, not controlled empirical proof.

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

The frozen B2 baseline is only the first prerequisite; the thesis is not yet validated.

## Current blockers / unknowns

- Context/instruction composition is not exposed natively in the currently normalized Claude CLI telemetry.
- Tool-schema contribution, accumulated tool-result/history contribution and detailed model/agent lineage are not yet fully attributed.
- Useful State Change and no-progress intervals remain unmeasured.
- Whether external instrumentation/control-plane overhead erodes savings remains unknown.
- Whether customers will pay for cross-provider runtime optimisation versus provider-native/gateway capabilities remains unproven.

## Immediate next work

1. Keep B2 Baseline v1 frozen at r02-r06; do not run r07 by default.
2. Execute Stage A of `experiments/B2_CONTEXT_INSTRUCTION_ATTRIBUTION_SPEC.md`: exhaust existing stream/artifact evidence before adding instrumentation.
3. Produce an attribution-gap table covering provider/system instructions, project instructions, task prompt, tool schemas, repo/file context, tool-result/history context, internal/subagent activity and residual runtime overhead.
4. Only if Stage A is insufficient, choose the smallest additional observation layer under `TELEMETRY_GAP_DECISION_PROTOCOL.md`.
5. Do not add OpenTelemetry, SDK wrappers or gateway instrumentation merely to improve completeness percentage.
6. After attribution, select exactly one isolated intervention according to measured evidence, not original list order.
7. Repeat the intervention sufficiently to compare distributions against frozen B2 Baseline v1 while enforcing deterministic non-inferiority and 100% tested mandatory compliance.
8. Continue competitor deep dives while runtime experiments progress.
9. Do not build a production control plane until measured baseline/intervention evidence supports it.
