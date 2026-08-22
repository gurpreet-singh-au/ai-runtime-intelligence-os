# B2 Context / Instruction Attribution Experiment

Experiment ID: `B2-ATTR-001`
Status: Designed; not yet executed
Depends on: frozen `B2 Baseline v1` (`r02`–`r06`)
Date: 2026-08-22

## Purpose

Determine what resource components are responsible for the large provider-reported cached-input processing observed during the small B2-001 bug-fix task, before attempting to optimise that footprint.

This is an **attribution experiment first**, not yet a savings claim and not yet a combined optimiser.

## Evidence motivating the experiment

The frozen B2 baseline v1 has five valid deterministic-success runs. Mean provider-reported cached-input processing is approximately 297,513 tokens, while mean fresh input is 1,087 tokens. Cached-input processing varies with CV approximately 11.84%, while fresh input varies with CV approximately 0.18%.

This establishes a resource-profile signal, but not its cause.

## Primary question

> Which observable source classes contribute materially to B2's processed context / cached-input footprint, and which of those classes are controllable without reducing task success or mandatory compliance?

## Attribution classes

Measure or estimate separately where technically possible:

1. provider/system instructions;
2. project/repository instructions and governance material;
3. task prompt;
4. exposed tool schemas/capability descriptions;
5. repository/file content supplied to the model;
6. conversation and prior tool-result history;
7. agent/subagent or internal utility activity;
8. other provider/runtime overhead that cannot be decomposed further.

Any unobservable class must remain `UNKNOWN`; do not infer zero.

## Hypotheses

### H1 — Controllable context/instruction mass exists

A material portion of the processed cached-input footprint is attributable to controllable project instructions, context selection, tool surface, or accumulated tool-result history.

### H2 — The dominant controllable source can be isolated

At least one source class can be reduced or compiled independently while holding the benchmark task, outcome evaluator, model/runtime configuration and mandatory rules constant.

### H3 — Savings can be achieved without outcome regression

A later isolated intervention against the dominant controllable source can materially reduce cost, processed tokens or latency while preserving 100% tested mandatory compliance and non-inferior parent-task quality.

H3 is **not tested by attribution alone**; it is the follow-on intervention hypothesis.

## Experimental sequence

### Stage A — Exhaust existing evidence first

Before adding instrumentation, inspect current Claude stream/artifacts and identify every attribution fact already recoverable from:

- `claude-stream.jsonl`;
- `STREAM_INVENTORY.json`;
- `normalized-run.json`;
- `RUN_METADATA.json`;
- tool-use blocks and tool-result events;
- model usage summaries;
- prompt and fixture files;
- runner behavior.

Produce an attribution-gap table with source class, directly observed evidence, inferred evidence, and unresolved fields.

### Stage B — Select the smallest additional observation layer

Only if Stage A cannot resolve the primary attribution question, evaluate observation options in this order:

1. richer native Claude/CLI output already available but not parsed;
2. native runtime telemetry such as OpenTelemetry if it exposes the required composition fields;
3. thin SDK/wrapper instrumentation;
4. gateway/proxy instrumentation;
5. alternate runtime solely for measurement if necessary.

Do **not** add instrumentation merely to increase the generic telemetry-completeness percentage.

For each candidate observation layer, record:

- fields gained;
- implementation effort;
- expected runtime overhead;
- risk of changing execution behavior;
- provider/framework coupling;
- portability;
- ability to preserve the frozen benchmark semantics.

### Stage C — Attribution capture

Run the smallest technically adequate diagnostic configuration sufficient to populate the attribution classes above.

If instrumentation changes runtime semantics enough that direct comparison to Baseline v1 is invalid, classify the result as diagnostic-only and do not calculate savings against the frozen baseline.

### Stage D — Choose exactly one isolated intervention

Select the intervention according to measured attribution, not prior preference. Candidate mappings include:

- project/instruction mass -> instruction applicability compilation;
- irrelevant repository context -> context utility selection;
- large exposed tool schema -> tool-surface reduction;
- accumulated tool-result history -> tool-result externalisation/summarisation;
- avoidable internal/subagent activity -> agent/model routing experiment;
- mostly provider/system overhead -> mark as currently non-controllable and redirect to another resource class.

No combined intervention is allowed until isolated effects are understood.

## Controls

Unless an attribution method technically requires otherwise, hold constant:

- B2-001 fixture;
- frozen task prompt;
- deterministic evaluator v1.1;
- Python 3.11.6 benchmark venv;
- pytest 9.1.1;
- Claude permission mode `acceptEdits`;
- model-selection/runtime settings used by the frozen baseline;
- benchmark success criteria.

Any deviation must be recorded as an experimental factor.

## Required telemetry

Minimum existing comparison metrics:

- total cost;
- runtime duration;
- fresh input tokens;
- cached-input tokens;
- cache-creation input tokens;
- output tokens;
- tool-call count and sequence;
- models observed;
- deterministic outcome.

Attribution-specific targets:

- context composition by source class;
- instruction composition by source class;
- tool-schema contribution where observable;
- tool-result/history contribution where observable;
- agent/subagent/internal utility lineage where observable;
- per-step processed-token or context-growth evidence where observable.

Missing fields remain `UNKNOWN`.

## Outcome evaluation

For any B2 intervention comparison, continue using the independent deterministic evaluator:

`experiments/adapters/claude_code/finalize_b2_outcome.py`

A valid successful intervention run requires all existing B2 checks to pass. Model self-report is not an outcome signal.

## Falsification / redirect criteria

The context/instruction hypothesis should be weakened or redirected if:

1. attribution shows that most processed cached-input mass is provider/runtime overhead outside project control;
2. removing/scoping the suspected source produces no material reduction beyond baseline variance;
3. any reduction causes test failure, out-of-scope diff or mandatory-compliance regression;
4. measurement overhead materially changes execution behavior or erases the apparent savings;
5. the measured effect is not distinguishable from baseline/intervention run-to-run variance after adequate repetition.

If (1) holds, move to another resource class rather than forcing a context-optimisation story.

## Comparison rule for the later intervention

Baseline reference: `B2 Baseline v1`, n=5.

Initial intervention target: five valid repetitions where economically practical. Compare distributions, not one-off best runs.

Primary decision metric remains risk-adjusted cost per successful parent outcome, with cost, latency, processed tokens and tool behavior as supporting measures.

A claimed win requires:

- 100% tested mandatory-rule compliance in the compared successful intervention set;
- non-inferior deterministic B2 outcome;
- material resource improvement relative to baseline distribution;
- no hidden transfer of cost into an unmeasured resource;
- clear documentation of measurement uncertainty and instrumentation overhead.

## Explicit non-goals

- proving the full AI Runtime Intelligence OS thesis;
- building a production control plane;
- choosing a permanent provider/framework;
- maximizing telemetry coverage for its own sake;
- optimizing multiple resource classes simultaneously;
- treating cache-read tokens as equivalent to unique useful context.

## Decision after this experiment

The experiment must end with one of three outcomes:

1. **PROCEED** — a dominant controllable source is identified and an isolated intervention is justified;
2. **REDIRECT** — the suspected context/instruction source is not dominant or controllable, so another resource class becomes the next target;
3. **INSUFFICIENT EVIDENCE** — attribution remains unresolved and a better measurement strategy is required before intervention.
