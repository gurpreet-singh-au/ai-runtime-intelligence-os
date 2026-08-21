# Project State — AI Runtime Intelligence OS

Last updated: 2026-08-22
Phase: Phase 0B — competitive boundary + experimental proof preparation
Status: Active; first benchmark tranche ready for runtime execution

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
- Local logic verification confirms the B2/B5 fixtures currently fail their intended acceptance conditions before repair, so they are suitable defect fixtures; this is not a model baseline result.
- Control maturity path remains: Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise.

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

Target repetitions: five per case where economically practical, with exact runtime/model/version and repository snapshot preserved.

No baseline model runs have yet been recorded. The current GitHub-connected environment can prepare and analyse benchmark artifacts but does not expose a local Claude Code process/runtime for running the repetitions.

## First empirical milestone

> On at least two representative workloads, demonstrate material compute/cost or latency reduction while maintaining non-inferior parent-task quality and 100% tested mandatory-rule compliance.

## Current blockers / unknowns

- Need an execution environment that can run the selected agent/runtime and expose/export enough raw telemetry for normalization.
- Exact native telemetry fields/hooks available from the chosen runtime need to be verified at execution time.
- Best practical source for context/instruction composition telemetry where providers expose only aggregate token counts.
- Whether task relevance and instruction applicability can be estimated reliably enough for safe automation.
- Whether Useful State Change can be measured consistently across heterogeneous tasks.
- Whether external control-plane/instrumentation overhead erodes savings.
- Whether customers will pay for cross-provider runtime optimisation versus provider-native/gateway capabilities.
- Whether any competitor already performs meaningful task-level multi-resource optimisation; competitor research remains ongoing.

## Immediate next work

1. Execute untouched baseline cycles for B2-001/B3-001/B5-001/B7-001 in a runtime-capable environment.
2. Preserve raw transcript/trace, provider usage, tool calls, test outputs, diffs and evaluator results for each run.
3. Normalize each run into `experiments/RUN_SCHEMA.json`, leaving genuinely unavailable fields null rather than inferring them.
4. Analyse variance and telemetry gaps before creating any optimizer intervention.
5. Repeat at least a subset of baselines on a materially different runtime/provider before making cross-provider claims.
6. Continue competitor deep dives into Portkey, LangSmith, AgentOps, RouteLLM, memory/context platforms and AI FinOps.
7. Do not build a production control plane until measured baseline/intervention evidence supports it.
