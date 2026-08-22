# B2-ATTR-001 Stage B Plan

Date: 2026-08-22
Experiment: `B2-ATTR-001`
Stage: B — smallest additional observation layer
Status: Designed; not yet executed
Depends on: `experiments/B2_ATTRIBUTION_STAGE_A_RESULT.md`

## Decision entering Stage B

Stage A exhausted the current Claude Code stream artifacts and resolved useful secondary questions, including explicit zero spawned subagents across the five valid baseline runs. It did **not** resolve the primary composition question: which source classes account for the repeated processed/cache footprint.

Stage B therefore begins with a **native telemetry capability audit**, not an optimisation intervention.

## Objective

Determine whether Claude Code's native OpenTelemetry monitoring can expose enough additional evidence to distinguish one or more of the unresolved composition classes without materially changing runtime semantics.

The unresolved target classes are:

1. provider/system instructions;
2. project/repository instructions and governance;
3. task prompt;
4. exposed tool schemas;
5. repository/file content;
6. conversation/tool-result history;
7. secondary/internal model activity lineage;
8. residual provider/runtime overhead.

## Why OpenTelemetry is evaluated first

Anthropic documentation identifies OpenTelemetry monitoring as a supported Claude Code observability mechanism. This makes it a lower-coupling candidate than introducing a custom SDK wrapper, proxy or gateway.

However, support for OpenTelemetry does **not** prove that it exposes prompt composition or source-class token attribution. The first Stage B task is therefore to inspect the actual available telemetry schema and payloads under the installed Claude Code version.

## Stage B1 — capability discovery

Do not run a full comparative experiment yet.

First determine, using the installed Claude Code version and official/runtime-exposed configuration, which OpenTelemetry signals are available and whether they include any of:

- model-request boundaries;
- per-request model identity;
- per-request input/cache/output usage;
- tool-use events;
- session/conversation identifiers;
- parent/child or internal-call lineage;
- prompt/system/tool-schema size or composition;
- context-window or compaction events;
- latency by model request;
- cost fields;
- error/retry events.

For every candidate field classify:

- `OBSERVED` — emitted directly;
- `DERIVED` — computed from observed fields;
- `UNAVAILABLE` — tested and not emitted;
- `UNKNOWN` — not yet tested.

Do not assume a documented metric exists in the installed version until observed locally.

## Stage B2 — minimal diagnostic capture

If B1 identifies useful telemetry, run **one diagnostic B2 capture** with telemetry enabled.

This diagnostic run is not part of frozen Baseline v1 and must use a separate identifier such as:

`B2-ATTR-001-otel-diagnostic-r01`

Hold the benchmark semantics constant where technically possible:

- B2 fixture and frozen task prompt;
- deterministic evaluator v1.1;
- Python 3.11.6 benchmark environment;
- pytest 9.1.1;
- Claude permission mode `acceptEdits`;
- normal model/runtime selection behavior.

Record any unavoidable configuration difference caused by telemetry.

## Diagnostic-only rule

Do **not** calculate savings against B2 Baseline v1 from the first telemetry-enabled run.

The first Stage B capture exists to answer:

1. what fields are gained;
2. whether they resolve the attribution question;
3. what telemetry overhead is introduced;
4. whether the execution trajectory appears materially changed.

Only after telemetry equivalence/overhead is understood may a telemetry-enabled configuration be used for comparative experiments.

## Privacy and evidence handling

Any telemetry that may contain prompts, repository text, tool inputs/results, file paths or code must remain local by default.

Do not commit raw diagnostic telemetry to GitHub. Commit only:

- schemas;
- redacted samples where necessary;
- aggregate findings;
- field-availability matrices;
- experiment decisions.

## Stage B exit criteria

Stage B ends with one of:

### B-PROCEED
Native telemetry exposes enough composition/lineage evidence to identify a plausible dominant controllable source. Design exactly one isolated intervention.

### B-ESCALATE
Native telemetry adds useful observability but still cannot resolve composition. Evaluate the next-smallest mechanism under `TELEMETRY_GAP_DECISION_PROTOCOL.md`, such as a thin SDK/wrapper.

### B-REDIRECT
Native evidence indicates the suspected context/instruction sources are not practically observable or controllable in this runtime. Redirect to another runtime resource class or use a different runtime as the measurement surface.

## Parallel cross-runtime lane

The project may prepare a separate Codex controlled-baseline adapter in parallel because Codex provides a valuable second runtime/provider observation surface. It must remain analytically separate from Claude B2 Baseline v1.

The same canonical B2 task semantics and independent deterministic outcome evaluator should be reused where technically compatible, while runtime-specific telemetry stays behind its own adapter.

The Codex lane is not a substitute for completing Claude Stage B; it is a cross-runtime validation lane for the provider-agnostic thesis.

## Guardrails

- No production control plane.
- No combined optimiser.
- No intervention before attribution evidence justifies it.
- No assumption that telemetry completeness equals usefulness.
- No assumption that a provider-specific observability field belongs in the canonical model unchanged.
- Any runtime-specific field must be mapped through a provider-neutral evidence layer.
