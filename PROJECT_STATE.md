# Project State — AI Runtime Intelligence OS

Last updated: 2026-08-21
Phase: Phase 0 — deep research and opportunity validation
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
- Initial experimental philosophy: baseline -> isolated intervention -> combined intervention -> quality-preserving evaluation.
- Control maturity path: Observe -> Explain -> Recommend -> Simulate -> Guardrail -> Auto-optimise.

## Current hypotheses

1. Long-running AI systems materially waste compute through oversized/stale context, over-broad instructions, repeated tool output, redundant agents, inappropriate model choice, and low-value runtime loops.
2. Provider-native features solve mechanisms but leave room for cross-provider intelligence that decides when/how to use those mechanisms.
3. Capability- and evaluation-driven routing can reduce cost without reducing successful parent-task outcomes.
4. Instruction compilation can reduce context load while preserving mandatory semantics and governance.
5. Marginal Compute Utility can become a useful decision abstraction for additional context, agents, searches, reasoning, and verification.
6. The first commercial wedge may be runtime observability/advisory for coding agents and long-running agent systems, but this remains unvalidated.

## Current blockers / unknowns

- Exact telemetry/intervention hooks available across Claude Code, OpenAI/Codex, Gemini and major agent frameworks.
- Whether task relevance and instruction applicability can be estimated reliably enough for safe automation.
- Whether external control-plane overhead erodes savings.
- Whether customers will pay for cross-provider runtime optimisation versus provider-native capabilities.
- Best first workload for reproducible experiments.

## Immediate next work

1. Complete market/competitor landscape from primary sources.
2. Define telemetry schema and minimum viable instrumentation.
3. Define representative benchmark task set.
4. Establish baseline metrics for context, agents, tools, cost, latency, quality, and outcome.
5. Design first advisory-only prototype experiment.
6. Maintain continuity and update this file after substantive work.
