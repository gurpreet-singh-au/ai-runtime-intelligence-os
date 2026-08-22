# Project State — AI Runtime Intelligence OS

Last updated: 2026-08-22
Phase: Phase 0B — competitive boundary + experimental proof preparation
Status: Claude B2 Baseline v1 frozen; Claude Stage B1/B2 complete with B-ESCALATE; Codex native-Windows discovery executed but bounded-write path blocked by workspace-write/read-only runtime defect

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
- Runtime-specific observations map through provider-neutral evidence rather than becoming architecture dependencies.
- Process exit `0` is not treated as task success; independent parent-task outcome evidence is mandatory.
- Requested runtime policy and effective runtime policy can diverge materially and must be measured separately.

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

## B2-ATTR-001 Stage A — COMPLETE

Formal result: `experiments/B2_ATTRIBUTION_STAGE_A_RESULT.md`.

Key findings:

1. Spawned subagents are OBSERVED absent across all five valid B2 baseline runs.
2. Secondary Haiku usage is small and highly stable.
3. Most observed cost/cache processing is associated with Sonnet.
4. Message-level cache-read snapshots grow from roughly 22k early to 35k–36k later.
5. Final 261k–336k cache-read totals represent repeated processing/reuse across turns, not a unique context size.
6. Native stream evidence cannot attribute system instructions, project instructions, tool schemas, file context, history and residual runtime overhead sufficiently.

Stage A decision: **INSUFFICIENT EVIDENCE FOR COMPOSITION ATTRIBUTION; PROCEED TO STAGE B.**

## B2-ATTR-001 Stage B1 — COMPLETE

Formal result: `experiments/B2_ATTRIBUTION_STAGE_B1_RESULT.md`.

Native OpenTelemetry was validated in the installed Claude Code 2.1.238 Windows environment through local OTLP transport and privacy-safe protobuf schema discovery.

Observed native signal classes include metrics, logs and traces. Useful fields include model identity, request/session IDs, request-level input/cache/output usage, cost, duration, TTFT, trace/parent linkage, prompt-length metadata and `llm_request.context` presence.

This justified one diagnostic-only telemetry-enabled B2 run.

## B2-ATTR-001 Stage B2 — COMPLETE

Formal result: `experiments/B2_ATTRIBUTION_STAGE_B2_RESULT.md`.

Run: `B2-ATTR-001-otel-diagnostic-r01`

The diagnostic passed the independent evaluator:

- `success: true`;
- `mandatory_compliance: true`.

### Mechanistic findings

- Parent task used **9 Sonnet requests** plus **1 Haiku request**.
- Haiku telemetry exposes `query_source = generate_session_title`; it is internal session-title generation, not a spawned task subagent.
- Sonnet cache-read progression: 22,115 -> 31,592 -> 33,764 -> 34,695 -> 35,217 -> 35,434 -> 35,555 -> 35,703 -> 35,904.
- Across every successive Sonnet request, the recurrence is exact:

`next cache_read = previous cache_read + previous cache_creation`

- This demonstrates stepwise cached-prefix carry-forward across the trajectory.
- First Sonnet request processed input: **31,594 tokens** (22,115 cache-read + 9,477 cache-create + 2 fresh).
- Final Sonnet request processed input: **36,096 tokens**.
- Post-first-request growth: **4,502 tokens**.
- First-request share of final processed input: **87.53%**.
- Post-first growth share: **12.47%**.

Interpretation: for B2, most of the final request footprint was already present at the first Sonnet request. Later tool/result/history growth is real but is not the dominant source of the final per-request footprint in this diagnostic.

### Native OTel boundary

`llm_request.context` was present but was only an 11-character non-JSON string for every Sonnet request. It did not expose actual request composition.

Therefore native OTel resolves request/cache mechanics but still cannot distinguish the initial large prefix among:

- provider/system/runtime instructions;
- tool schemas/tool capability surface;
- project/repository instructions;
- task prompt;
- other provider/runtime material.

Stage B2 decision: **B-ESCALATE.**

## Current highest-value Claude question

What makes up the approximately 31.6k-token first Sonnet processed input, especially the 22.1k cached prefix and 9.5k newly cached material?

The next Claude measurement mechanism should be the smallest local, reversible request-inspection layer capable of reporting outbound request structure and sizes without persisting raw prompt, code, tool-result or repository content.

Do not make that diagnostic mechanism a product dependency by default.

## Cross-runtime lane — Codex

Plan: `experiments/CODEX_B2_CONTROLLED_BASELINE_PLAN.md`.
Formal discovery result: `experiments/CODEX_B2_DISCOVERY_RESULT.md`.

### Capability discovery

Installed runtime:

- `codex-cli 0.144.3`
- non-interactive `exec` available
- JSON/JSONL output available
- explicit sandbox options available
- model/config controls available

### Discovery runs

- `B2-001-codex-discovery-r01` — aborted before meaningful task execution because a known shared-model-cache stderr diagnostic was promoted by PowerShell into a terminating native-command error.
- `B2-001-codex-discovery-r02` — same class of harness/native-stderr abort; wrapper switch alone was insufficient.
- `B2-001-codex-discovery-r03` — Codex model turn executed and process exited `0`, but effective workspace behavior remained read-only despite explicit `--sandbox workspace-write`.

### r03 observed evidence

Structured events:

- `thread.started`
- `turn.started`
- one `item.completed` of type `agent_message`
- `turn.completed`

No `command_execution` event.
No `file_change` event.
No tracked source-code diff.

Native Codex usage exposed:

- input tokens: **9,010**
- cached input tokens: **0**
- output tokens: **46**
- reasoning output tokens: **0**

The agent explicitly reported the workspace as read-only and did not inspect/edit the benchmark.

Pre-tests failed as expected; post-tests still failed. The deterministic evaluator correctly returned failure.

The apparent `workspace_modified: true` signal was caused only by untracked Python `__pycache__` directories generated by test execution, not a benchmark code change.

### Working diagnosis

The local observation closely matches active upstream OpenAI Codex issue `#34961`: native Windows `codex exec --sandbox workspace-write` can exit successfully while behaving read-only.

A separate upstream issue `#39291` documents the observed `models_cache.json` / missing `base_instructions` compatibility warning; r03 nevertheless reached a complete model turn, so that warning is no longer the primary blocker.

### Codex decision

- Do **not** weaken to `danger-full-access` merely to force a successful sample.
- Do **not** count r01-r03 as Codex baseline observations.
- Native-Windows Codex remains discovery-blocked for bounded-write B2 execution.
- Preferred next path: detect whether an already-available WSL/Linux Codex environment exists; if so, validate bounded-write semantics with a minimal synthetic write probe before running B2.
- Do not automatically install, upgrade, or copy authentication material as part of the experiment.
- Treat any runtime upgrade as an explicit experimental-factor change and re-probe before comparing results.

## Competitive/commercial boundary — UPDATED

Current direct/near-direct findings include:

- Not Diamond Code — coding-agent session/cache-aware model and reasoning-effort optimisation.
- cascadeflow — MIT-licensed agent runtime intelligence/harness with model cascading, budget/compliance/KPI controls, tool-call limits and runtime decisions including allow/switch-model/deny-tool/stop.
- established observability/evaluation/gateway layers including Langfuse, LangSmith, Braintrust, Portkey, OpenRouter and others.

The phrase/category `agent runtime intelligence layer` is therefore not unique territory.

The remaining potentially defensible hypothesis is narrower: **provider-neutral cross-resource allocation under a common governed outcome/economic objective**, including context, instructions, models/reasoning, tools, agents, memory, verification and time.

Formal commercial re-audit: `research/COMMERCIAL_DEFENSIBILITY_REAUDIT_2026-08-22.md`.

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

## Immediate next work

1. Keep Claude B2 Baseline v1 frozen at r02-r06.
2. Treat Claude Stage B2 as B-ESCALATE; do not run more OTel probes merely for completeness.
3. Detect whether an already-available WSL/Linux Codex path exists without installing or copying credentials; if present, run a minimal bounded-write capability probe before B2.
4. Do not weaken native-Windows Codex to `danger-full-access` merely to obtain a successful benchmark sample.
5. In parallel, design the smallest Claude outbound-request structure inspector; do not persist raw sensitive request content.
6. Continue competitor/open-source teardown, especially cascadeflow and Not Diamond Code, focusing on implemented algorithms rather than marketing claims.
7. Do not select a Claude optimisation intervention until initial-prefix composition is identified or a deliberate redirect is made.
8. Do not build a production control plane yet.
