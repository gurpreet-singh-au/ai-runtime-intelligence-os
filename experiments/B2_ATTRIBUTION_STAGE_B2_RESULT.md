# B2-ATTR-001 Stage B2 Result

Date: 2026-08-22
Experiment: `B2-ATTR-001`
Stage: B2 — privacy-safe native OTel B2 diagnostic
Run: `B2-ATTR-001-otel-diagnostic-r01`
Decision: **B-ESCALATE — native OTel resolves request/cache mechanics but not initial-prefix source composition**

## Outcome validity

The diagnostic reused the frozen B2-001 task semantics and independent deterministic evaluator.

Observed evaluator result:

- `success: true`;
- `mandatory_compliance: true`.

The run remains diagnostic-only and is not pooled into Claude B2 Baseline v1 and is not eligible for a savings claim.

## Runtime trajectory observed

The diagnostic captured:

- 9 Sonnet model requests for the parent B2 task;
- 1 Haiku request;
- native request/trace linkage;
- per-request cache read, cache creation, fresh input, output, duration, TTFT and cost fields;
- interaction-level timing;
- privacy-safe context-field metadata.

### Sonnet cache trajectory

Per-request cache-read tokens:

1. 22,115
2. 31,592
3. 33,764
4. 34,695
5. 35,217
6. 35,434
7. 35,555
8. 35,703
9. 35,904

Per-request cache-creation tokens:

1. 9,477
2. 2,172
3. 931
4. 522
5. 217
6. 121
7. 148
8. 201
9. 190

The recurrence is exact across every successive Sonnet request:

`next cache_read = previous cache_read + previous cache_creation`

Examples:

- 22,115 + 9,477 = 31,592;
- 31,592 + 2,172 = 33,764;
- 35,703 + 201 = 35,904.

This demonstrates a stepwise cached-prefix carry-forward mechanism across the task trajectory.

It does **not** identify the semantic/source composition of that prefix.

## Initial-prefix dominance

Processed input for the first Sonnet request:

- cache read: 22,115;
- cache creation: 9,477;
- fresh input: 2;
- total provider-accounted processed input: **31,594 tokens**.

Processed input for the final Sonnet request:

- cache read: 35,904;
- cache creation: 190;
- fresh input: 2;
- total: **36,096 tokens**.

Therefore:

- growth after the first Sonnet request: **4,502 tokens**;
- first-request processed-input share of final request: **87.53%**;
- post-first growth share: **12.47%**.

Interpretation guardrail: this is provider token accounting for individual requests, not a claim about unique semantic context size.

### Why this matters

For this B2 task, the majority of the final request's processed context footprint was already present on the **first Sonnet request**, before the later tool/result trajectory accumulated.

This materially narrows the optimisation question. Tool-result/history growth exists, but it is not the dominant source of the final per-request footprint in this run.

The highest-value unresolved question is now the composition of the approximately 31.6k-token first Sonnet processed input, especially the approximately 22.1k cache-read prefix and 9.5k newly cached material.

## Haiku purpose resolved

The secondary Haiku request is explicitly associated in native telemetry with:

`query_source = generate_session_title`

Therefore, for this diagnostic and consistent with Stage A's zero-subagent telemetry, the Haiku request is an internal session-title generation operation rather than spawned task-subagent work.

Its small footprint remains analytically separate from the parent Sonnet task trajectory.

## `llm_request.context` result

Native OTel exposes an `llm_request.context` attribute, but in every Sonnet request in this diagnostic it was:

- a string;
- 11 characters long;
- not JSON parseable.

The privacy-safe collector therefore obtained no composition structure from this field.

Native OTel does not expose enough information here to attribute the initial cached prefix among:

- provider/system instructions;
- Claude Code runtime instructions;
- tool schemas/tool capability surface;
- project/repository instructions;
- frozen task prompt;
- other provider/runtime material.

## Sonnet diagnostic totals

Observed across the 9 Sonnet requests:

- cache-read tokens: **299,979**;
- cache-creation tokens: **13,979**;
- fresh input tokens: **18**;
- output tokens: **1,309**;
- summed request duration: **19,633 ms**;
- summed request cost: **USD 0.1935567**.

These are diagnostic measurements only. Do not use this single telemetry-enabled run as evidence of savings/regression versus Baseline v1.

## Stage B2 decision

Native OTel has now answered valuable mechanistic questions:

- request boundaries: OBSERVED;
- model identity: OBSERVED;
- request-level cache/input/output usage: OBSERVED;
- request/interaction trace linkage: OBSERVED;
- cache-prefix carry-forward: DERIVED with exact arithmetic support;
- secondary Haiku purpose: OBSERVED (`generate_session_title`).

But it still cannot answer the primary source-composition question:

> What makes up the large initial Sonnet prefix before task-specific trajectory growth?

Therefore the Stage B exit is:

**B-ESCALATE.**

## Next Claude measurement target

Evaluate the smallest controlled request-inspection mechanism that can observe **structure and size of the outbound model request before transmission**, while avoiding persistence of raw sensitive content.

The target evidence should distinguish, where technically possible:

1. system/runtime instruction payload;
2. task/user prompt payload;
3. tool-schema payload;
4. conversation/message history;
5. tool-result blocks;
6. repository/project-instruction material;
7. other request fields.

Prefer local, reversible, diagnostic-only instrumentation. Do not make a gateway, proxy or SDK wrapper a product dependency merely because it is useful for measurement.

## Parallel Codex lane

The Claude attribution question should no longer block cross-runtime evidence collection.

Proceed in parallel with the already-designed Codex discovery lane under `experiments/CODEX_B2_CONTROLLED_BASELINE_PLAN.md`.

The first Codex run remains discovery-only and must validate Windows sandbox/write behavior, CLI/runtime version, authentication path, JSON event capture, test environment and deterministic evaluator compatibility before any Codex baseline is frozen.

## Guardrails

- Do not claim the initial 31.6k processed input is all unnecessary or controllable.
- Do not infer semantic composition from cache accounting alone.
- Do not persist raw prompt/context/tool/repository content merely to improve attribution.
- Do not pool the diagnostic run into Baseline v1.
- Do not select an optimisation intervention until the controllable composition is identified or a deliberate redirect decision is made.
