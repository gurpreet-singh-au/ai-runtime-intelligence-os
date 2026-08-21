# Baseline Tranche 01 — Passive Observation Plan

Date: 2026-08-22
Status: Ready for execution; no baseline model runs recorded yet

## Objective

Collect untouched baseline executions for B2-001, B3-001, B5-001 and B7-001 before applying Runtime Intelligence interventions.

## First runtime selection

**Provisional first runtime: Claude Code / Claude coding-agent workflow, passive observation only.**

Reason:
- the project was partly motivated by observed long-context, long-duration and subagent-heavy Claude coding sessions;
- coding/repository tasks match B2, B3 and B5 naturally;
- B7 directly tests subagent economics;
- using the motivating runtime first provides a high-signal validation target.

This is an experimental starting runtime, **not** an architectural dependency or preferred production provider. The benchmark suite must later be repeated on at least one materially different runtime/provider before cross-provider claims are made.

## Instrumentation principle

Prefer native/exported telemetry and passive wrappers. Do not modify the agent's decision policy during baseline collection.

The collector should populate `experiments/RUN_SCHEMA.json` using only data that is actually observable. Unknown fields remain `null`; do not fabricate token attribution, relevance or causal contribution.

### Required baseline fields

At minimum capture:
- benchmark ID and run ID;
- exact repository commit / fixture snapshot;
- runtime and runtime version where available;
- provider/model/version where exposed;
- start/end time;
- model-call counts where observable;
- input/cached/output usage where exposed;
- agent/subagent counts where observable;
- tool calls and tool names;
- test/search/file-read repetition where observable;
- total reported cost where available;
- deterministic outcome/evaluator result;
- raw evidence/artifact references.

### Inferred fields

These must be labelled as inferred or remain null until a defensible method exists:
- relevant-context tokens;
- stale/duplicate semantic context;
- useful state changes;
- no-progress semantic intervals;
- agent unique information contribution;
- marginal compute utility.

## Baseline policy freeze

For each case:
- use the normal runtime configuration;
- do not deliberately compact, clear, prune, restrict tools or change models mid-run for efficiency;
- do not manually prevent native subagent spawning;
- do not inject Runtime Intelligence recommendations;
- do not intentionally make the baseline inefficient;
- allow only normal safety/governance intervention.

## Repetitions

Initial target: five runs per benchmark if cost/time remains reasonable.

Execution order should rotate across cases rather than completing all repetitions of one case first, to reduce time/order confounding:

1. B2-001 r01
2. B3-001 r01
3. B5-001 r01
4. B7-001 r01
5. repeat cycle for r02 ... r05

If runtime/provider versions change during collection, record the change and do not silently pool incompatible runs.

## Deterministic evaluation

### B2-001
Run pricing tests. Success requires all targeted tests pass without weakening tests.

### B3-001
Use a frozen rubric evaluating factual correctness, repository grounding, citation precision, unsupported inference and unnecessary source reads.

### B5-001
Run retry tests. Success requires all targeted tests pass and no unnecessary unrelated change.

### B7-001
Use a frozen synthesis rubric covering all four required subquestions, competitor-fairness, fact/hypothesis separation, failure case and narrow remaining differentiation.

## Evidence retention

Per run preserve where available:
- raw runtime transcript/export;
- provider usage record;
- tool-call trace;
- changed-file diff for coding cases;
- test output;
- evaluator output;
- normalized run JSON.

Raw evidence is immutable for analysis purposes. Derived summaries may be regenerated.

## Execution limitation in this repository session

The repository and benchmark fixtures can be prepared here, but this GitHub-connected session does not itself expose a local Claude Code process/runtime on which to execute the five baseline repetitions. Therefore **no baseline result is claimed yet**.

The next execution step must occur in an environment that can run the selected agent/runtime and export or capture its telemetry. Once raw run artifacts exist, they should be normalized into this repository's run schema and analysed here.

## First analysis after baseline collection

For each case compute:
- success rate and variance;
- reported cost and latency distributions;
- model/agent/tool-call distributions;
- repeated file/search/test operations;
- context/usage growth where observable;
- run-to-run variability;
- evidence gaps caused by unavailable telemetry.

Only after baseline stability is understood should isolated interventions begin.
