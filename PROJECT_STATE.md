# Project State — AI Runtime Intelligence OS

Last updated: 2026-08-21
Phase: Phase 0B — competitive boundary + experimental proof design
Status: Active

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
- Competitive/adjacent landscape now documented in `research/MARKET_LANDSCAPE.md` and `research/COMPETITOR_MATRIX.md`.
- Current competitor finding: observability, evaluation, gateway routing, reliability, budgets and agent/tool governance already exist in adjacent platforms; the project must prove additional value in cross-resource task planning and runtime allocation rather than duplicate that plumbing.
- Canonical provider-neutral telemetry model defined in `architecture/TELEMETRY_MODEL.md`.
- Benchmark and baseline experiment design defined in `research/BENCHMARK_AND_BASELINE_SPEC.md`.
- Experimental harness documentation and machine-readable run schema started under `experiments/`.
- Initial experimental philosophy: baseline -> isolated intervention -> combined intervention -> quality-preserving evaluation.
- Control maturity path: Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise.

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

Start with:
- B2 — small bug fix;
- B3 — repository research;
- B5 — debug/test loop;
- B7 — multi-agent decomposable research.

Baseline = normal/default runtime execution with passive telemetry only.

First empirical milestone:

> On at least two representative workloads, demonstrate material compute/cost or latency reduction while maintaining non-inferior parent-task quality and 100% tested mandatory-rule compliance.

## Current blockers / unknowns

- Exact telemetry/intervention hooks available across Claude Code, OpenAI/Codex, Gemini and major agent frameworks.
- Best practical source for context/instruction composition telemetry where providers expose only aggregate token counts.
- Whether task relevance and instruction applicability can be estimated reliably enough for safe automation.
- Whether Useful State Change can be measured consistently across heterogeneous tasks.
- Whether external control-plane/instrumentation overhead erodes savings.
- Whether customers will pay for cross-provider runtime optimisation versus provider-native/gateway capabilities.
- Whether any competitor already performs meaningful task-level multi-resource optimisation; competitor research is incomplete.

## Immediate next work

1. Convert the four benchmark families into concrete reproducible test cases and acceptance criteria.
2. Select one first runtime/adaptor for passive telemetry only; do not make it foundational.
3. Determine what telemetry can be collected natively versus through OpenTelemetry/vendor adapters versus a lightweight custom wrapper.
4. Run baseline experiments before any optimiser intervention.
5. Continue competitor deep dives into Portkey, LangSmith, AgentOps, RouteLLM, memory/context platforms and AI FinOps.
6. Update evidence/source registers with all material primary sources and record unknowns explicitly.
7. Do not build a production control plane until measured baseline/intervention evidence supports it.
