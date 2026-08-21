# Reproducible Benchmark Cases

Status: Phase 0B experimental tranche 1

These cases instantiate B2, B3, B5 and B7 from `research/BENCHMARK_AND_BASELINE_SPEC.md`.

## Baseline rule

Run each case with the chosen runtime's normal/default behaviour and **passive observation only**. Do not intentionally reduce context, tools, agents, reasoning, retries or verification during baseline runs.

Each baseline configuration should be repeated at least five times where economically practical. Record each run using `experiments/RUN_SCHEMA.json`.

## B2-001 — Small bug fix: order discount

Fixture: `benchmarks/fixtures/python_runtime_fixture/`

Objective:
- diagnose the failing pricing tests;
- make the smallest correct code change;
- do not weaken/delete tests;
- run the relevant tests.

Known acceptance criteria:
- all `tests/test_pricing.py` tests pass;
- discount applies to merchandise subtotal only;
- shipping remains undiscounted;
- existing validation behaviour remains intact.

Primary measurements:
- files/searches read before root cause;
- model/tool calls;
- context and instruction load;
- repeated reads/tests;
- elapsed time and cost;
- success on deterministic tests.

Risk class: low.

## B3-001 — Repository research: runtime resource model

Target repository: this repository, pinned to the run's starting commit.

Question:

> Explain how the project distinguishes cache efficiency from cognitive/context efficiency, identify the canonical runtime resource classes directly implicated by that distinction, and cite the minimum repository evidence needed to support the answer.

Acceptance criteria:
- correctly distinguishes cheaper reuse from whether information should be model-visible;
- identifies relevant resource classes without inventing classes;
- cites repository paths/sections supporting the answer;
- marks unsupported inference as inference;
- does not modify repository files.

Primary measurements:
- number of file searches/reads;
- duplicate reads;
- total retrieved bytes/tokens if observable;
- context growth;
- agent/subagent count;
- evidence precision (useful sources / sources opened);
- final grounding/quality.

Risk class: low.

## B5-001 — Debug/test loop: retry boundary

Fixture: `benchmarks/fixtures/python_runtime_fixture/`

Objective:
- diagnose the failing retry-policy test;
- correct the defect without changing the public contract;
- run the relevant tests;
- stop when acceptance criteria are satisfied.

Acceptance criteria:
- all `tests/test_retry.py` tests pass;
- no retry occurs after the configured maximum number of total attempts;
- non-transient statuses are not retried;
- no unnecessary unrelated refactor.

Why this case exists:
The code defect is small, but the benchmark is intended to measure whether an agent enters repeated test/read/edit loops after sufficient evidence exists.

Primary measurements:
- repeated tests;
- repeated reads of unchanged files;
- repeated unsuccessful strategies;
- no-progress intervals;
- time/cost to deterministic success.

Risk class: low.

## B7-001 — Multi-agent decomposable research

Question:

> Assess whether a provider-independent Runtime Intelligence layer has a plausible defensible role above existing AI observability, evaluation and gateway products. Produce a structured answer covering: (A) observability/evaluation, (B) model/provider gateways, (C) agent governance, and (D) the remaining cross-resource optimisation hypothesis. Synthesize only after the four subquestions are investigated.

Evidence set:
- repository research documents, especially `research/MARKET_LANDSCAPE.md`, `research/COMPETITOR_MATRIX.md`, `research/OPENROUTER_AND_MODEL_ROUTING.md`, and the architecture/resource documents;
- current primary vendor sources may be used when the benchmark protocol explicitly allows fresh web retrieval.

Acceptance criteria:
- four subquestions are substantively addressed;
- competitor capabilities are not understated merely to create a gap;
- conclusions distinguish established facts from project hypotheses;
- identifies at least one reason the thesis could fail;
- identifies the narrowest remaining differentiation hypothesis;
- final synthesis is internally consistent and evidence-backed.

Experimental purpose:
Compare parent-only, baseline/native multi-agent, reduced-agent and capability-routed variants. Measure unique information gain, overlap and coordination cost rather than rewarding raw agent count.

Risk class: low.

## Repetition IDs

Use run IDs such as:

`B2-001-baseline-r01`
`B2-001-baseline-r02`
...

Intervention variants should name the intervention explicitly, for example:

`B7-001-agent-reduction-r01`
`B7-001-capability-routing-r01`

## Freeze rule

Once baseline collection begins for a case, the task prompt, fixture snapshot, acceptance criteria and evaluator version must be pinned. Material changes create a new benchmark version rather than silently modifying the old one.
