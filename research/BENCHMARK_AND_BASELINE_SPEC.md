# Benchmark & Baseline Experiment Specification

Date: 2026-08-21
Status: Phase 0 experimental design v0.1

## Purpose

Define representative workloads and a reproducible baseline so runtime-efficiency claims can be tested rather than inferred from anecdotal token/cost reports.

## Governing rule

No intervention is successful merely because it reduces tokens, agents, calls, runtime or cost.

An intervention must preserve or improve the required outcome quality, reliability, safety and mandatory-rule compliance for the task class.

## Primary metric

**Risk-adjusted cost per successful parent outcome**.

Supporting metrics:
- parent-task success rate;
- quality score;
- mandatory-rule compliance;
- total model cost;
- latency;
- context load;
- instruction load;
- agent/subagent count;
- tool calls and repeated tool calls;
- verification cost;
- Useful State Change Rate;
- runtime waste ratio.

## Benchmark workload families

### B1 — Trivial deterministic code/repository task

Example shape:
- locate one known config value;
- modify one bounded file;
- run a deterministic validation.

Why included:
Tests whether models/agents are unnecessarily used for work that can be deterministic or highly bounded.

Risk: low.

### B2 — Small bug fix

Example shape:
- reproduce a scoped defect;
- identify root cause;
- change 1–3 files;
- run targeted tests.

Why included:
Representative coding-agent workload with real reasoning but limited scope.

Risk: low/medium depending on repository.

### B3 — Repository research / question answering

Example shape:
- answer an architecture or behaviour question from a medium/large repository;
- cite relevant files/lines;
- no production change.

Why included:
Tests selective retrieval, repeated reads/searches, context growth and subagent research behaviour.

### B4 — Multi-file feature implementation

Example shape:
- implement a clearly specified feature touching multiple components;
- tests required;
- documentation/state update required.

Why included:
Tests long context, planning, agent delegation, tool/result accumulation and verification.

### B5 — Debug/test loop

Example shape:
- start from failing tests or a reproducible error;
- diagnose and iterate until acceptance criteria pass.

Why included:
Likely to expose runtime loops, repeated test output, repeated file reads and no-progress intervals.

### B6 — Deep research synthesis

Example shape:
- answer a technical market/research question using multiple authoritative sources;
- distinguish fact/inference/unknown;
- produce evidence-backed synthesis.

Why included:
Tests search/tool economics, evidence externalisation, context selection and verifier value.

### B7 — Multi-agent decomposable research task

Example shape:
- several genuinely separable subquestions;
- final parent synthesis required.

Why included:
Tests whether additional subagents create unique information, correlated duplication, or coordination overhead.

### B8 — High-consequence / governance-sensitive simulation

Use synthetic or non-sensitive scenarios requiring mandatory policy checks and stronger verification.

Why included:
Ensures the optimiser learns that more compute/verification can be efficient when consequences justify it.

No real-world harmful or irreversible actions are part of the benchmark.

## Workload selection for first experimental tranche

Start with four workloads:

1. B2 — small bug fix;
2. B3 — repository research;
3. B5 — debug/test loop;
4. B7 — multi-agent research.

Reason: these are likely to reveal the context, tool and subagent waste patterns that motivated the project while remaining practical to evaluate.

## Reproducibility requirements

Each benchmark case must pin:

```yaml
benchmark_id:
task_family:
repository_or_dataset_snapshot:
commit_or_version:
objective:
acceptance_criteria:
risk_class:
mandatory_instructions:
allowed_tools:
provider:
model:
model_version:
agent_runtime:
runtime_version:
starting_state:
time_budget:
cost_budget:
evaluator_version:
```

Where external web information is required, preserve source URLs/versions/retrieval dates and recognise that perfect replay may not be possible.

## Baseline policy

The baseline is **normal/default execution** for the selected runtime, with no Runtime Intelligence intervention beyond passive telemetry.

Do not intentionally make the baseline inefficient.

Record native/default:
- model choice;
- reasoning settings;
- agent/subagent behaviour;
- context management;
- tool availability;
- retry/fallback behaviour;
- compaction/checkpoint behaviour.

## Baseline repetitions

Because model execution is stochastic, one run is insufficient.

Initial research target:
- minimum 5 repetitions per benchmark/configuration where economically practical;
- more repetitions for noisy outcomes before commercial claims;
- record variance and confidence intervals rather than only averages.

The exact sample size should be revised after observing variance.

## Evaluation model

Use the strongest practical deterministic evaluator first.

Evaluation layers:

1. deterministic acceptance tests / unit tests / schema validators;
2. evidence/citation validation where applicable;
3. rubric-based evaluator model where semantic quality is required;
4. independent model/provider check for selected experiments;
5. human review only where necessary for research validity or risk governance.

Do not use the same model-generated self-assessment as the sole evidence of success.

## Outcome record

Every run should produce:

```yaml
run_id:
benchmark_id:
policy_variant:
success:
quality_score:
mandatory_compliance:
latency_ms:
input_tokens:
cached_tokens:
output_tokens:
model_calls:
agent_count:
tool_calls:
repeated_tool_calls:
context_peak:
instruction_tokens:
verification_cost:
total_cost:
useful_state_changes:
no_progress_intervals:
evaluator_notes:
```

## Isolated intervention experiments

### I1 — Context selection

Compare:
- baseline context policy;
- selective task-relevant context;
- checkpoint + clean retrieval.

Hypothesis:
Reduce context/prefill cost without non-inferior outcome loss.

### I2 — Instruction compilation

Compare:
- full applicable instruction universe;
- deduplicated/scoped compiled instructions.

Hard gate:
100% mandatory-rule inclusion/compliance in deterministic tests.

### I3 — Dynamic tool exposure

Compare:
- full tool surface;
- capability-routed minimal surface.

Measure:
selection accuracy, schema load, calls, failures, outcome.

### I4 — Tool-result externalisation

Compare:
- raw result retained in hot context;
- raw evidence stored externally + compact structured working state.

### I5 — Agent-count optimisation

Compare:
- baseline agent spawning;
- fewer agents;
- diverse vs homogeneous agents where relevant;
- parent-only execution where feasible.

Measure unique contribution and parent outcome, not merely agent cost.

### I6 — Subagent model routing

Compare:
- parent/frontier model for all agents;
- fixed cheaper model for low-risk subtasks;
- capability/eval-driven model routing;
- free-model lane only for pre-qualified low-risk tasks where available and policy-permitted.

### I7 — Deterministic substitution

Replace model calls with deterministic software for mechanical operations where possible.

### I8 — Loop/no-progress intervention

Test detection of:
- repeated searches/reads/tests;
- token growth without meaningful state change;
- repeated failed strategies.

Intervention modes:
- advisory only first;
- checkpoint/change-strategy simulation next.

### I9 — Model/reasoning routing

Compare model tier and reasoning effort according to task complexity/risk.

### I10 — Verification allocation

Compare minimum, baseline and risk-adjusted verification depth.

Important: this intervention may deliberately increase compute on high-risk cases.

## Combined policy experiment

Only after isolated interventions are understood:

`Task profile -> compiled context/instructions -> model route -> agent topology -> tool surface -> runtime/stop policy -> verification plan`

Compare against baseline on parent outcome, total cost, latency and risk-adjusted utility.

## Non-inferiority rules

### Ordinary low/medium-risk tasks

A cheaper policy must show non-inferior outcome quality within a predeclared tolerance.

Do not define the tolerance after seeing results.

### High-risk simulations

Require stricter quality/compliance thresholds; cost reduction is secondary.

### Mandatory governance

Any material mandatory-rule compliance regression fails the intervention regardless of savings.

## Candidate derived metrics

### Cost per successful outcome

`total cost / successful parent outcomes`

### Risk-adjusted cost per successful outcome

Conceptual form:

`total resource cost + expected failure/risk penalty` divided by successful outcomes.

Do not operationalise the risk penalty until a defensible method is defined.

### Context Utility Density

`estimated task-relevant context / physical model-visible context`

### Useful State Change Rate

`meaningful state changes / compute or elapsed time`

### Runtime Waste Ratio

Candidate components:
- repeated operations;
- redundant agent work;
- stale/duplicate context;
- invalid/retried structured outputs;
- no-progress intervals;
- unnecessary model calls.

Do not combine into one score until weights are empirically justified.

### Agent Marginal Utility

`incremental parent-outcome value attributable to agent / incremental agent resource cost`

Requires careful experimental design; trace correlation alone is not causal attribution.

## First empirical milestone

The first milestone is intentionally modest:

> On at least two representative workloads, demonstrate a material reduction in compute/cost or latency while maintaining non-inferior parent-task quality and 100% tested mandatory-rule compliance.

Until this occurs, the Runtime Intelligence commercial thesis remains an unvalidated hypothesis.

## Next implementation artifact

Before running experiments, create a lightweight `experiments/README.md` and a machine-readable run schema based on `architecture/TELEMETRY_MODEL.md`.

Do not build the production control plane yet.
