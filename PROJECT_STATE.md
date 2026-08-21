# Project State — AI Runtime Intelligence OS

Last updated: 2026-08-22
Phase: Phase 0B — competitive boundary + experimental proof preparation
Status: Active; first valid B2 baseline captured and awaiting baseline-repetition decision

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
- Deep research tranches started on context, caching, inference, tools, agents, memory, runtime, and economics.
- Competitive/adjacent landscape documented in `research/MARKET_LANDSCAPE.md` and `research/COMPETITOR_MATRIX.md`.
- Current competitor finding: observability, evaluation, gateway routing, reliability, budgets and agent/tool governance already exist in adjacent platforms; the project must prove additional value in cross-resource task planning and runtime allocation rather than duplicate that plumbing.
- Canonical provider-neutral telemetry model defined in `architecture/TELEMETRY_MODEL.md`.
- Benchmark and baseline experiment design defined in `research/BENCHMARK_AND_BASELINE_SPEC.md`.
- Machine-readable experiment run schema defined in `experiments/RUN_SCHEMA.json`.
- Concrete benchmark cases B2-001, B3-001, B5-001 and B7-001 defined in `benchmarks/README.md`.
- Deterministic Python fixtures created for B2-001 and B5-001 under `benchmarks/fixtures/python_runtime_fixture/`.
- Semantic evaluator rubrics created for B3-001 and B7-001 under `experiments/evaluators/`.
- First passive baseline tranche documented in `experiments/BASELINE_TRANCHE_01.md` and `experiments/baseline_tranche_01_manifest.json`.
- Provisional first observation runtime: Claude Code / Claude coding-agent workflow, selected as an experimental starting point because it matches the motivating workload. This is not an architectural dependency or permanent provider decision.
- Claude Code passive-observation harness created under `experiments/adapters/claude_code/`.
- The Windows harness now uses a benchmark-local Python 3.11 virtual environment with pinned pytest and `acceptEdits` for non-interactive benchmark file edits.
- A conservative normalization pipeline converts raw Claude run artifacts into provider-neutral `normalized-run.json` plus `TELEMETRY_COMPLETENESS.json` without turning missing telemetry into zero.
- Token normalization now prefers the final `result.modelUsage` summary rather than recursively double-counting message/result/iteration usage.
- `experiments/TELEMETRY_GAP_DECISION_PROTOCOL.md` governs whether native CLI evidence is sufficient or requires OpenTelemetry, gateway/proxy, SDK instrumentation, or a different runtime.
- Control maturity path remains: Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise.

## First empirical captures

### B2-001-baseline-r01 — discovery / invalid baseline

- Captured useful native Claude Code stream evidence, but the run is not a valid baseline.
- Two harness defects were discovered:
  1. plain `python` resolved to an unrelated Hermes virtual environment without pytest;
  2. Claude Code non-interactive execution used default permissions, so the correct `Edit` operation was denied twice.
- The trace showed Claude correctly diagnosed the pricing defect and proposed the intended minimal fix, but no file change was applied.
- Preserve r01 as instrumentation/environment discovery evidence; do not include it in baseline performance statistics.

### B2-001-baseline-r02 — first valid candidate baseline

Environment:
- Claude Code 2.1.238
- benchmark-local Python 3.11.6 venv
- pytest 9.1.1
- permission mode `acceptEdits`
- source repository commit `1358d0516957951e51be1ec1028ab74a8eb302b1`

Outcome:
- pre-test: 2 failed, 1 passed;
- Claude exit code: 0;
- post-test: 3 passed;
- diff: only `runtime_fixture/pricing.py`, with the intended minimal correction so shipping is added after the merchandise discount;
- therefore B2-001 r02 is the first valid successful baseline candidate.

Observed native telemetry:
- aggregate input tokens: 1,085;
- cache-read input tokens: 262,353;
- cache-creation input tokens: 13,224;
- output tokens: 1,154;
- tool calls: 8;
- Claude result duration: 20,054 ms;
- total reported cost: USD 0.1763469;
- observed models: `claude-sonnet-5` and `claude-haiku-4-5-20251001`;
- telemetry completeness under current required-field rubric: 0.4667.

Important interpretation constraints:
- cache token counts are provider-reported processed/cache usage, not unique semantic context size;
- context composition, instruction composition, useful state change, repeated-operation structure and some model/agent lineage fields remain UNKNOWN;
- one successful run is not enough to estimate variance or claim optimisation savings.

## Current differentiation hypotheses to prove

1. Task Resource Profiling can estimate useful resource requirements before execution.
2. Instruction Applicability Compilation can reduce instruction load without governance regression.
3. Context Utility Allocation can reduce stale/duplicate context while preserving evidence and outcome quality.
4. Agent Spawn Economics can decide whether another subagent is justified before paying for it.
5. Marginal Compute Utility can compare the value of additional context, reasoning, agents, searches, tools and verification.
6. Useful State Change / Loop Intelligence can identify low-progress runtime trajectories earlier than generic tracing alone.
7. Execution Counterfactuals can identify which resources contributed materially to success.
8. Outcome-Conditioned Policy Learning can learn task fingerprint -> execution strategy mappings across providers and runtimes.

## First benchmark tranche

Concrete cases:
- B2-001 — small bug fix: order discount;
- B3-001 — repository research: cache efficiency vs cognitive/context efficiency;
- B5-001 — debug/test loop: retry boundary;
- B7-001 — multi-agent decomposable competitive-boundary research.

Baseline = normal/default runtime execution with passive telemetry only.

Target repetitions: five valid runs per case where economically practical, revised if observed variance justifies a different sample size.

## First empirical milestone

> On at least two representative workloads, demonstrate material compute/cost or latency reduction while maintaining non-inferior parent-task quality and 100% tested mandatory-rule compliance.

## Current blockers / unknowns

- Need deterministic outcome finalization wired into normalized run artifacts rather than requiring manual interpretation of test outputs.
- Need to decide whether native CLI telemetry is sufficient for B2 baseline repetitions despite 46.67% completeness, or whether missing fields are material to the specific B2 hypothesis.
- Context/instruction composition is not exposed natively in the current CLI stream.
- Useful State Change and no-progress intervals remain unmeasured.
- Need baseline variance before any cost/latency improvement claim.
- Whether external control-plane/instrumentation overhead erodes savings remains unknown.
- Whether customers will pay for cross-provider runtime optimisation versus provider-native/gateway capabilities remains unproven.

## Immediate next work

1. Treat B2-001 r02 as the first valid successful baseline candidate; exclude r01 from baseline statistics.
2. Add deterministic B2 outcome finalization so `normalized-run.json` records success/compliance from test exit metadata and bounded diff evidence.
3. Apply the telemetry-gap decision protocol specifically to B2: distinguish fields required for this benchmark from fields that can remain UNKNOWN without invalidating baseline repetitions.
4. If B2 native telemetry is sufficient, collect additional valid B2 baseline repetitions and quantify variance before intervention testing.
5. Do not add OpenTelemetry solely to increase a generic completeness percentage; add instrumentation only if required by the hypothesis under test.
6. After a stable B2 baseline distribution exists, begin one isolated intervention at a time rather than a combined optimiser.
7. Continue competitor deep dives while runtime experiments progress.
8. Do not build a production control plane until measured baseline/intervention evidence supports it.
